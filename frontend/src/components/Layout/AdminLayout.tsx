import { useState } from 'react'
import { Layout, Menu, Avatar, Dropdown, Space } from 'antd'
import {
  UserOutlined,
  TeamOutlined,
  LogoutOutlined,
  DashboardOutlined,
} from '@ant-design/icons'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { logout } from '../../store/authSlice'
import type { RootState } from '../../store'
import type { MenuProps } from 'antd'

const { Header, Sider, Content } = Layout

const API_URL = '/api'

const AdminLayout = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const dispatch = useDispatch()
  const { user, token } = useSelector((state: RootState) => state.auth)

  const menuItems: MenuProps['items'] = [
    { key: '/admin', icon: <DashboardOutlined />, label: 'Обзор' },
    { key: '/admin/users', icon: <UserOutlined />, label: 'Пользователи' },
    { key: '/admin/groups', icon: <TeamOutlined />, label: 'Группы' },
  ]

  const userMenuItems: MenuProps['items'] = [
    { key: 'logout', icon: <LogoutOutlined />, label: 'Выход', danger: true },
  ]

  const handleMenuClick = ({ key }: { key: string }) => navigate(key)

  const handleUserMenuClick = async ({ key }: { key: string }) => {
    if (key === 'logout') {
      try {
        await fetch(`${API_URL}/auth/users/logout/`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
        })
      } catch (_) {}
      dispatch(logout())
      navigate('/login')
    }
  }

  const displayName = user
    ? (user.first_name && user.last_name ? `${user.first_name} ${user.last_name}` : user.username)
    : 'Администратор'

  const avatarSrc = (user as any)?.avatar_url || undefined

  return (
    <Layout className="app-layout">
      <Sider
        breakpoint="lg"
        collapsedWidth="0"
        style={{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0, top: 0, bottom: 0 }}
      >
        <div style={{ height: 64, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#fff', fontSize: 18, fontWeight: 'bold' }}>
          КЦП О-2М
        </div>
        <div style={{ padding: '8px 16px', color: '#aaa', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1 }}>
          Администрирование
        </div>
        <Menu
          theme="dark"
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Sider>

      <Layout style={{ marginLeft: 200 }}>
        <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', justifyContent: 'flex-end', alignItems: 'center' }}>
          <Dropdown menu={{ items: userMenuItems, onClick: handleUserMenuClick }} placement="bottomRight">
            <Space style={{ cursor: 'pointer' }}>
              <Avatar src={avatarSrc} icon={!avatarSrc && <UserOutlined />} />
              <span>{displayName}</span>
              <span style={{ fontSize: 11, color: '#888', background: '#f0f0f0', padding: '2px 8px', borderRadius: 10 }}>Администратор</span>
            </Space>
          </Dropdown>
        </Header>

        <Content className="app-content">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}

export default AdminLayout
