import { useState } from 'react'
import { Layout, Menu, Avatar, Dropdown, Space } from 'antd'
import {
  DashboardOutlined,
  CameraOutlined,
  RocketOutlined,
  WifiOutlined,
  CalendarOutlined,
  FileTextOutlined,
  UserOutlined,
  LogoutOutlined,
} from '@ant-design/icons'
import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { logout } from '../../store/authSlice'
import type { RootState } from '../../store'
import type { MenuProps } from 'antd'
import ProfileDrawer from '../../pages/Profile'

const { Header, Sider, Content } = Layout

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const AppLayout = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const dispatch = useDispatch()
  const { user, token } = useSelector((state: RootState) => state.auth)
  const [profileOpen, setProfileOpen] = useState(false)

  const menuItems: MenuProps['items'] = [
    { key: '/', icon: <DashboardOutlined />, label: 'Главная' },
    { key: '/requests', icon: <CameraOutlined />, label: 'Заявки на съёмку' },
    { key: '/satellites', icon: <RocketOutlined />, label: 'Космические аппараты' },
    { key: '/ground-stations', icon: <WifiOutlined />, label: 'Наземные станции' },
    { key: '/planning', icon: <CalendarOutlined />, label: 'Планирование' },
    { key: '/flight-tasks', icon: <FileTextOutlined />, label: 'Полётные задания' },
  ]

  const userMenuItems: MenuProps['items'] = [
    { key: 'profile', icon: <UserOutlined />, label: 'Профиль' },
    { key: 'logout', icon: <LogoutOutlined />, label: 'Выход', danger: true },
  ]

  const handleMenuClick = ({ key }: { key: string }) => navigate(key)

  const handleUserMenuClick = async ({ key }: { key: string }) => {
    if (key === 'profile') {
      setProfileOpen(true)
    } else if (key === 'logout') {
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
    : 'Пользователь'

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
            </Space>
          </Dropdown>
        </Header>

        <Content className="app-content">
          <Outlet />
        </Content>
      </Layout>

      <ProfileDrawer open={profileOpen} onClose={() => setProfileOpen(false)} />
    </Layout>
  )
}

export default AppLayout
