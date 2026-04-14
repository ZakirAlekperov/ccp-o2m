import { useState, useRef } from 'react'
import {
  Drawer, Avatar, Button, Form, Input,
  Divider, Typography, Upload, message,
  Tag, Space
} from 'antd'
import {
  UserOutlined, EditOutlined, LockOutlined,
  UploadOutlined, SaveOutlined, CloseOutlined
} from '@ant-design/icons'
import { useDispatch, useSelector } from 'react-redux'
import { loginSuccess } from '../store/authSlice'
import type { RootState } from '../store'

const { Title, Text } = Typography

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const ROLE_COLORS: Record<string, string> = {
  admin: 'red',
  operator: 'blue',
  analyst: 'green',
  viewer: 'default',
}

interface ProfileDrawerProps {
  open: boolean
  onClose: () => void
}

const ProfileDrawer = ({ open, onClose }: ProfileDrawerProps) => {
  const dispatch = useDispatch()
  const { user, token } = useSelector((state: RootState) => state.auth)
  const [editMode, setEditMode] = useState(false)
  const [pwdMode, setPwdMode] = useState(false)
  const [loading, setLoading] = useState(false)
  const [profileForm] = Form.useForm()
  const [pwdForm] = Form.useForm()
  const fileInputRef = useRef<HTMLInputElement>(null)

  if (!user) return null

  const authHeaders = { Authorization: `Bearer ${token}` }

  // ---- helpers ----

  const refreshUser = async () => {
    const res = await fetch(`${API_URL}/auth/users/me/`, { headers: authHeaders })
    const data = await res.json()
    dispatch(loginSuccess({ user: data, token: token! }))
  }

  // ---- save profile ----

  const handleSaveProfile = async (values: Record<string, string>) => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/auth/users/me/update/`, {
        method: 'PATCH',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      })
      const data = await res.json()
      if (!res.ok) {
        const firstError = Object.values(data)[0]
        message.error(Array.isArray(firstError) ? firstError[0] : String(firstError))
        return
      }
      dispatch(loginSuccess({ user: data, token: token! }))
      message.success('Профиль обновлён')
      setEditMode(false)
    } finally {
      setLoading(false)
    }
  }

  // ---- change password ----

  const handleChangePassword = async (values: Record<string, string>) => {
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/auth/users/me/change-password/`, {
        method: 'POST',
        headers: { ...authHeaders, 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      })
      const data = await res.json()
      if (!res.ok) {
        const firstError = Object.values(data)[0]
        message.error(Array.isArray(firstError) ? firstError[0] : String(firstError))
        return
      }
      // Update token after password change
      dispatch(loginSuccess({ user: user, token: data.access_token }))
      message.success('Пароль изменён')
      pwdForm.resetFields()
      setPwdMode(false)
    } finally {
      setLoading(false)
    }
  }

  // ---- avatar upload ----

  const handleAvatarChange = async (file: File) => {
    const formData = new FormData()
    formData.append('avatar', file)
    setLoading(true)
    try {
      const res = await fetch(`${API_URL}/auth/users/me/avatar/`, {
        method: 'PATCH',
        headers: authHeaders,
        body: formData,
      })
      const data = await res.json()
      if (!res.ok) { message.error('Ошибка загрузки'); return }
      dispatch(loginSuccess({ user: data, token: token! }))
      message.success('Аватарка обновлена')
    } finally {
      setLoading(false)
    }
  }

  const displayName = (user.first_name && user.last_name)
    ? `${user.first_name} ${user.last_name}`
    : user.username

  const avatarSrc = (user as any).avatar_url || undefined

  return (
    <Drawer
      title="Профиль пользователя"
      placement="right"
      width={420}
      open={open}
      onClose={() => { setEditMode(false); setPwdMode(false); onClose() }}
    >
      {/* Avatar block */}
      <div style={{ textAlign: 'center', marginBottom: 24 }}>
        <div style={{ position: 'relative', display: 'inline-block' }}>
          <Avatar
            size={96}
            src={avatarSrc}
            icon={!avatarSrc && <UserOutlined />}
            style={{ cursor: 'pointer' }}
            onClick={() => fileInputRef.current?.click()}
          />
          <Button
            size="small"
            shape="circle"
            icon={<UploadOutlined />}
            style={{ position: 'absolute', bottom: 0, right: 0 }}
            onClick={() => fileInputRef.current?.click()}
          />
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            style={{ display: 'none' }}
            onChange={(e) => {
              const file = e.target.files?.[0]
              if (file) handleAvatarChange(file)
            }}
          />
        </div>
        <div style={{ marginTop: 12 }}>
          <Title level={4} style={{ margin: 0 }}>{displayName}</Title>
          <Text type="secondary">@{user.username}</Text>
          <br />
          <Tag color={ROLE_COLORS[user.role] || 'default'} style={{ marginTop: 6 }}>
            {user.role_display}
          </Tag>
        </div>
      </div>

      <Divider />

      {/* Profile info / edit */}
      {!editMode ? (
        <>
          <Space direction="vertical" style={{ width: '100%' }} size={8}>
            <Text type="secondary">Имя</Text>
            <Text>{user.first_name || '—'}</Text>
            <Text type="secondary">Фамилия</Text>
            <Text>{user.last_name || '—'}</Text>
            <Text type="secondary">Логин</Text>
            <Text>{user.username}</Text>
            <Text type="secondary">Email</Text>
            <Text>{user.email || '—'}</Text>
          </Space>
          <Button
            icon={<EditOutlined />}
            style={{ marginTop: 16, width: '100%' }}
            onClick={() => {
              profileForm.setFieldsValue({
                first_name: user.first_name,
                last_name: user.last_name,
                username: user.username,
                email: user.email,
              })
              setEditMode(true)
            }}
          >
            Редактировать
          </Button>
        </>
      ) : (
        <Form form={profileForm} layout="vertical" onFinish={handleSaveProfile}>
          <Form.Item name="first_name" label="Имя">
            <Input />
          </Form.Item>
          <Form.Item name="last_name" label="Фамилия">
            <Input />
          </Form.Item>
          <Form.Item
            name="username"
            label="Логин"
            rules={[{ required: true, message: 'Обязательное поле' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item name="email" label="Email">
            <Input type="email" />
          </Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" icon={<SaveOutlined />} loading={loading}>
              Сохранить
            </Button>
            <Button icon={<CloseOutlined />} onClick={() => setEditMode(false)}>
              Отмена
            </Button>
          </Space>
        </Form>
      )}

      <Divider />

      {/* Password change */}
      {!pwdMode ? (
        <Button
          icon={<LockOutlined />}
          style={{ width: '100%' }}
          onClick={() => setPwdMode(true)}
        >
          Изменить пароль
        </Button>
      ) : (
        <Form form={pwdForm} layout="vertical" onFinish={handleChangePassword}>
          <Form.Item
            name="current_password"
            label="Текущий пароль"
            rules={[{ required: true }]}
          >
            <Input.Password prefix={<LockOutlined />} />
          </Form.Item>
          <Form.Item
            name="new_password"
            label="Новый пароль"
            rules={[{ required: true, min: 8, message: 'Минимум 8 символов' }]}
          >
            <Input.Password prefix={<LockOutlined />} />
          </Form.Item>
          <Form.Item
            name="confirm_password"
            label="Подтвердите пароль"
            rules={[{ required: true }]}
          >
            <Input.Password prefix={<LockOutlined />} />
          </Form.Item>
          <Space>
            <Button type="primary" htmlType="submit" loading={loading}>
              Сохранить
            </Button>
            <Button onClick={() => { pwdForm.resetFields(); setPwdMode(false) }}>
              Отмена
            </Button>
          </Space>
        </Form>
      )}
    </Drawer>
  )
}

export default ProfileDrawer
