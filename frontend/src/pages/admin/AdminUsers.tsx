import { useEffect, useState } from 'react'
import {
  Table, Tag, Button, Space, Modal, Form, Input, Select,
  Typography, Spin, Alert, Popconfirm, message,
} from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { useSelector } from 'react-redux'
import type { RootState } from '../../store'
import type { ColumnsType } from 'antd/es/table'

const { Title } = Typography
const API_URL = '/api'

interface UserRecord {
  id: number
  username: string
  email: string
  first_name: string
  last_name: string
  role: string
  role_display: string
  is_active: boolean
}

interface Group {
  id: number
  name: string
}

const AdminUsers = () => {
  const { token } = useSelector((state: RootState) => state.auth)
  const [users, setUsers] = useState<UserRecord[]>([])
  const [groups, setGroups] = useState<Group[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingUser, setEditingUser] = useState<UserRecord | null>(null)
  const [form] = Form.useForm()

  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }

  const fetchAll = async () => {
    try {
      setLoading(true)
      const [uRes, gRes] = await Promise.all([
        fetch(`${API_URL}/auth/users/`, { headers }),
        fetch(`${API_URL}/auth/groups/`, { headers }),
      ])
      if (!uRes.ok) throw new Error('Ошибка загрузки пользователей')
      const uData = await uRes.json()
      const gData = gRes.ok ? await gRes.json() : []
      setUsers(Array.isArray(uData) ? uData : uData.results ?? [])
      setGroups(Array.isArray(gData) ? gData : gData.results ?? [])
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchAll() }, [])

  const openCreate = () => {
    setEditingUser(null)
    form.resetFields()
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
      const url = editingUser
        ? `${API_URL}/auth/users/${editingUser.id}/`
        : `${API_URL}/auth/users/`
      const method = editingUser ? 'PATCH' : 'POST'
      const res = await fetch(url, { method, headers, body: JSON.stringify(values) })
      if (!res.ok) throw new Error('Ошибка сохранения')
      message.success(editingUser ? 'Пользователь обновлён' : 'Пользователь создан')
      setModalOpen(false)
      fetchAll()
    } catch (e: any) {
      message.error(e.message)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await fetch(`${API_URL}/auth/users/${id}/`, { method: 'DELETE', headers })
      if (!res.ok) throw new Error('Ошибка удаления')
      message.success('Пользователь удалён')
      fetchAll()
    } catch (e: any) {
      message.error(e.message)
    }
  }

  const columns: ColumnsType<UserRecord> = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    { title: 'Логин', dataIndex: 'username' },
    { title: 'Email', dataIndex: 'email' },
    {
      title: 'Имя',
      render: (_, r) => `${r.first_name} ${r.last_name}`.trim() || '—',
    },
    {
      title: 'Группа / Роль',
      dataIndex: 'role_display',
      render: (val) => <Tag color="blue">{val}</Tag>,
    },
    {
      title: 'Статус',
      dataIndex: 'is_active',
      render: (v) => v ? <Tag color="green">Активен</Tag> : <Tag color="red">Неактивен</Tag>,
    },
    {
      title: 'Действия',
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(record)}>Изменить</Button>
          <Popconfirm title="Удалить пользователя?" onConfirm={() => handleDelete(record.id)}>
            <Button size="small" danger icon={<DeleteOutlined />}>Удалить</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ]

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 80, textAlign: 'center' }} />
  if (error) return <Alert type="error" message={error} style={{ margin: 24 }} />

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
        <Title level={3} style={{ margin: 0 }}>Пользователи</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={openCreate}>Добавить</Button>
      </div>

      <Table rowKey="id" columns={columns} dataSource={users} />

      <Modal
        title={editingUser ? 'Редактировать пользователя' : 'Новый пользователь'}
        open={modalOpen}
        onOk={handleSave}
        onCancel={() => setModalOpen(false)}
        okText="Сохранить"
        cancelText="Отмена"
      >
        <Form form={form} layout="vertical">
          <Form.Item name="username" label="Логин" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          {!editingUser && (
            <Form.Item name="password" label="Пароль" rules={[{ required: true }]}>
              <Input.Password />
            </Form.Item>
          )}
          <Form.Item name="email" label="Email" rules={[{ type: 'email' }]}>
            <Input />
          </Form.Item>
          <Form.Item name="first_name" label="Имя">
            <Input />
          </Form.Item>
          <Form.Item name="last_name" label="Фамилия">
            <Input />
          </Form.Item>
          <Form.Item name="role" label="Группа / Роль">
            <Select
              options={[
                { value: 'operator', label: 'Оператор' },
                { value: 'admin', label: 'Администратор' },
                ...groups
                  .filter(g => g.name !== 'operator' && g.name !== 'admin')
                  .map(g => ({ value: g.name, label: g.name })),
              ]}
            />
          </Form.Item>
          <Form.Item name="is_active" label="Статус" initialValue={true}>
            <Select options={[
              { value: true, label: 'Активен' },
              { value: false, label: 'Неактивен' },
            ]} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default AdminUsers
