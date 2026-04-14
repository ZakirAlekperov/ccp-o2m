import { useEffect, useState } from 'react'
import {
  Table, Button, Space, Modal, Form, Input,
  Typography, Spin, Alert, Popconfirm, message, Tag,
} from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { useSelector } from 'react-redux'
import type { RootState } from '../../store'
import type { ColumnsType } from 'antd/es/table'

const { Title, Text } = Typography
const API_URL = '/api'

interface Group {
  id: number
  name: string
  permissions?: string[]
}

const SYSTEM_GROUPS = ['operator', 'admin']

const AdminGroups = () => {
  const { token } = useSelector((state: RootState) => state.auth)
  const [groups, setGroups] = useState<Group[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [modalOpen, setModalOpen] = useState(false)
  const [editingGroup, setEditingGroup] = useState<Group | null>(null)
  const [form] = Form.useForm()

  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' }

  const fetchGroups = async () => {
    try {
      setLoading(true)
      const res = await fetch(`${API_URL}/auth/groups/`, { headers })
      if (!res.ok) throw new Error('Ошибка загрузки групп')
      const data = await res.json()
      setGroups(Array.isArray(data) ? data : data.results ?? [])
    } catch (e: any) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetchGroups() }, [])

  const openCreate = () => {
    setEditingGroup(null)
    form.resetFields()
    setModalOpen(true)
  }

  const openEdit = (group: Group) => {
    setEditingGroup(group)
    form.setFieldsValue(group)
    setModalOpen(true)
  }

  const handleSave = async () => {
    try {
      const values = await form.validateFields()
      const url = editingGroup
        ? `${API_URL}/auth/groups/${editingGroup.id}/`
        : `${API_URL}/auth/groups/`
      const method = editingGroup ? 'PATCH' : 'POST'
      const res = await fetch(url, { method, headers, body: JSON.stringify(values) })
      if (!res.ok) throw new Error('Ошибка сохранения')
      message.success(editingGroup ? 'Группа обновлена' : 'Группа создана')
      setModalOpen(false)
      fetchGroups()
    } catch (e: any) {
      message.error(e.message)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      const res = await fetch(`${API_URL}/auth/groups/${id}/`, { method: 'DELETE', headers })
      if (!res.ok) throw new Error('Ошибка удаления')
      message.success('Группа удалена')
      fetchGroups()
    } catch (e: any) {
      message.error(e.message)
    }
  }

  const columns: ColumnsType<Group> = [
    { title: 'ID', dataIndex: 'id', width: 60 },
    {
      title: 'Название',
      dataIndex: 'name',
      render: (name) => (
        <Space>
          <span>{name}</span>
          {SYSTEM_GROUPS.includes(name) && <Tag color="orange">Системная</Tag>}
        </Space>
      ),
    },
    {
      title: 'Действия',
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<EditOutlined />} onClick={() => openEdit(record)}>Изменить</Button>
          {!SYSTEM_GROUPS.includes(record.name) && (
            <Popconfirm title="Удалить группу?" onConfirm={() => handleDelete(record.id)}>
              <Button size="small" danger icon={<DeleteOutlined />}>Удалить</Button>
            </Popconfirm>
          )}
        </Space>
      ),
    },
  ]

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 80, textAlign: 'center' }} />
  if (error) return <Alert type="error" message={error} style={{ margin: 24 }} />

  return (
    <div style={{ padding: 24 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <Title level={3} style={{ margin: 0 }}>Группы пользователей</Title>
        <Button type="primary" icon={<PlusOutlined />} onClick={openCreate}>Добавить группу</Button>
      </div>
      <Text type="secondary" style={{ display: 'block', marginBottom: 16 }}>
        Системные группы (operator, admin) нельзя удалить.
      </Text>

      <Table rowKey="id" columns={columns} dataSource={groups} />

      <Modal
        title={editingGroup ? 'Редактировать группу' : 'Новая группа'}
        open={modalOpen}
        onOk={handleSave}
        onCancel={() => setModalOpen(false)}
        okText="Сохранить"
        cancelText="Отмена"
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="Название группы" rules={[{ required: true, message: 'Введите название' }]}>
            <Input placeholder="например: analyst" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default AdminGroups
