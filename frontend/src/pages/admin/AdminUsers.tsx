import { useEffect, useState } from 'react'
import {
  Table, Tag, Button, Space, Modal, Form, Input, Select,
  Typography, Spin, Alert, Popconfirm, message, Badge, Avatar,
} from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, UserOutlined } from '@ant-design/icons'
import { useSelector } from 'react-redux'
import type { RootState } from '../../store'
import type { ColumnsType } from 'antd/es/table'

const { Title, Text } = Typography
const API_URL = '/api'

const ROLE_OPTIONS = [
  { value: 'admin',    label: 'Администратор' },
  { value: 'operator', label: 'Оператор' },
  { value: 'analyst',  label: 'Аналитик' },
  { value: 'viewer',   label: 'Наблюдатель' },
]
const ROLE_COLOR: Record<string, string> = {
  admin: 'red', operator: 'blue', analyst: 'purple', viewer: 'default',
}

interface UserRecord {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  role: string
  role_display: string
  is_active: boolean
  avatar_url?: string
}

const AdminUsers = () => {
  const { token } = useSelector((state: RootState) => state.auth)
  const [users, setUsers] = useState<UserRecord[]>([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingUser, setEditingUser] = useState<UserRecord | null>(null)
  const [form] = Form.useForm()

  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }

  const fetchUsers = async () => {
    try {
      setLoading(true)
      const res = await fetch(`${API_URL}/auth/users/`, { headers })
      if (!res.ok) throw new Error('Ошибка загрузки пользователей')
      const data = await res.json()
      setUsers(Array.isArray(data) ? data : data.results ?? [])
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchUsers() }, [])

  const openCreate = () => {
    setEditingUser(null)
    form.resetFields()
    form.setFieldsValue({ is_active: true, role: 'operator' })
    setModalOpen(true)
  }

  const openEdit = (user: UserRecord) => {
    setEditingUser(user)
    form.setFieldsValue(user)
    setModalOpen(true)
  }

  const handleSave = async () => {
    try {
      const values = await form.validateFields()
      setSaving(true)
      const url    = editingUser ? `${API_URL}/auth/users/${editingUser.id}/` : `${API_URL}/auth/users/`
      const method = editingUser ? 'PATCH' : 'POST'
      const res = await fetch(url, { method, headers, body: JSON.stringify(values) })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(Object.values(err).flat().join('; '))
      }
      message.success(editingUser ? 'Пользователь обновлён' : 'Пользователь создан')
      setModalOpen(false)
      fetchUsers()
    } catch (e: any) {
      message.error(e.message)
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await fetch(`${API_URL}/auth/users/${id}/`, { method: 'DELETE', headers })
      if (!res.ok) throw new Error('Ошибка удаления')
      message.success('Пользователь удалён')
      fetchUsers()
    } catch (e: any) {
      message.error(e.message)
    }
  }

  const columns: ColumnsType<UserRecord> = [
    {
      title: 'Пользователь',
      render: (_, r) => (
        <Space>
          <Avatar src={r.avatar_url} icon={<UserOutlined />} size={32} />
          <div>
            <div><Text strong>{r.username}</Text></div>
            <div><Text type="secondary" style={{ fontSize: 12 }}>{r.email || '—'}</Text></div>
          </div>
        </Space>
      ),
    },
    {
      title: 'Полное имя',
      render: (_, r) => {
        const name = `${r.first_name} ${r.last_name}`.trim()
        return name || <Text type="secondary">—</Text>
      },
    },
    {
      title: 'Роль',
      dataIndex: 'role',
      filters: ROLE_OPTIONS.map(o => ({ text: o.label, value: o.value })),
      onFilter: (value, record) => record.role === value,
      render: (v, r) => <Tag color={ROLE_COLOR[v] ?? 'default'}>{r.role_display || v}</Tag>,
    },
    {
      title: 'Статус',
      dataIndex: 'is_active',
      filters: [{ text: 'Активен', value: true }, { text: 'Неактивен', value: false }],
      onFilter: (value, record) => record.is_active === value,
      render: (v) => v
        ? <Badge status="success" text="Активен" />
        : <Badge status="error"   text="Неактивен" />,
    },
    {
      title: '',
      width: 160,
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(record)}>
            Изменить
          </Button>
          <Popconfirm
            title="Удалить пользователя?"
            description="Действие необратимо."
            okText="Удалить"
            okButtonProps={{ danger: true }}
            cancelText="Отмена"
            onConfirm={() => handleDelete(record.id)}
          >
            <Button size="small" danger icon={<DeleteOutlined />} />
          </Popconfirm>
        </Space>
      ),
    },
  ]

  if (loading) return <Spin size="large" style={{ display: 'block', margin: '80px auto' }} />
  if (error)   return <Alert type="error" message={error} style={{ margin: 24 }} />

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={4} style={{ margin: 0 }}>Пользователи</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={openCreate}>
          Добавить пользователя
        </Button>
      </div>

      <Table
        rowKey="id"
        columns={columns}
        dataSource={users}
        size="middle"
        pagination={{ pageSize: 20, showTotal: (t) => `Всего: ${t}` }}
      />

      <Modal
        title={editingUser ? 'Редактировать пользователя' : 'Новый пользователь'}
        open={modalOpen}
        onOk={handleSave}
        confirmLoading={saving}
        onCancel={() => setModalOpen(false)}
        okText="Сохранить"
        cancelText="Отмена"
        width={520}
        destroyOnClose
      >
        <Form form={form} layout="vertical" style={{ marginTop: 16 }}>
          <Form.Item name="username" label="Логин" rules={[{ required: true, message: 'Введите логин' }]}>
            <Input autoComplete="off" />
          </Form.Item>
          {!editingUser && (
            <Form.Item name="password" label="Пароль" rules={[{ required: true, message: 'Введите пароль' }]}>
              <Input.Password autoComplete="new-password" />
            </Form.Item>
          )}
          <Form.Item name="email" label="Email" rules={[{ type: 'email', message: 'Некорректный email' }]}>
            <Input />
          </Form.Item>
          <Space style={{ width: '100%' }} size={12}>
            <Form.Item name="first_name" label="Имя" style={{ flex: 1, marginBottom: 0 }}>
              <Input />
            </Form.Item>
            <Form.Item name="last_name" label="Фамилия" style={{ flex: 1, marginBottom: 0 }}>
              <Input />
            </Form.Item>
          </Space>
          <Form.Item name="role" label="Роль" style={{ marginTop: 16 }} rules={[{ required: true }]}>
            <Select options={ROLE_OPTIONS} />
          </Form.Item>
          <Form.Item name="is_active" label="Статус">
            <Select options={[
              { value: true,  label: 'Активен' },
              { value: false, label: 'Неактивен' },
            ]} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default AdminUsers
