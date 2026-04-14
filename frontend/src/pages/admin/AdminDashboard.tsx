import { useEffect, useState } from 'react'
import { Row, Col, Card, Statistic, Typography, Spin, Alert, Table, Tag, Badge } from 'antd'
import {
  UserOutlined, TeamOutlined, RocketOutlined,
  WifiOutlined, CameraOutlined, ClockCircleOutlined,
} from '@ant-design/icons'
import { useSelector } from 'react-redux'
import type { RootState } from '../../store'
import { useNavigate } from 'react-router-dom'

const { Title, Text } = Typography
const API_URL = '/api'

const ROLE_COLOR: Record<string, string> = {
  admin:    'red',
  operator: 'blue',
  analyst:  'purple',
  viewer:   'default',
}
const ROLE_LABEL: Record<string, string> = {
  admin:    'Администратор',
  operator: 'Оператор',
  analyst:  'Аналитик',
  viewer:   'Наблюдатель',
}

const AdminDashboard = () => {
  const { token } = useSelector((state: RootState) => state.auth)
  const navigate = useNavigate()
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [stats, setStats] = useState({
    users: 0, satellites: 0, groundStations: 0, requests: 0,
  })
  const [recentUsers, setRecentUsers] = useState<any[]>([])
  const [roleStats, setRoleStats] = useState<{ role: string; count: number }[]>([])

  const headers = { Authorization: `Bearer ${token}` }

  useEffect(() => {
    const load = async () => {
      try {
        const [uRes, sRes, gsRes, rRes] = await Promise.all([
          fetch(`${API_URL}/auth/users/`,       { headers }),
          fetch(`${API_URL}/satellites/`,       { headers }),
          fetch(`${API_URL}/ground-stations/`,  { headers }),
          fetch(`${API_URL}/imaging-requests/`, { headers }),
        ])
        const users      = uRes.ok  ? await uRes.json()  : []
        const satellites = sRes.ok  ? await sRes.json()  : []
        const gs         = gsRes.ok ? await gsRes.json() : []
        const requests   = rRes.ok  ? await rRes.json()  : []

        const uArr  = Array.isArray(users)      ? users      : users.results      ?? []
        const sArr  = Array.isArray(satellites) ? satellites : satellites.results ?? []
        const gsArr = Array.isArray(gs)         ? gs         : gs.results         ?? []
        const rArr  = Array.isArray(requests)   ? requests   : requests.results   ?? []

        setStats({
          users:          uArr.length,
          satellites:     sArr.length,
          groundStations: gsArr.length,
          requests:       rArr.length,
        })

        setRecentUsers([...uArr].reverse().slice(0, 5))

        const roleCounts: Record<string, number> = {}
        uArr.forEach((u: any) => { roleCounts[u.role] = (roleCounts[u.role] ?? 0) + 1 })
        setRoleStats(Object.entries(roleCounts).map(([role, count]) => ({ role, count })))
      } catch (e: any) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [token])

  if (loading) return <Spin size="large" style={{ display: 'block', margin: '80px auto' }} />
  if (error)   return <Alert type="error" message={error} style={{ margin: 24 }} />

  const statCards = [
    { title: 'Пользователи',     value: stats.users,          icon: <UserOutlined />,   color: '#1677ff', link: '/admin/users' },
    { title: 'Группы / роли',    value: roleStats.length,     icon: <TeamOutlined />,   color: '#52c41a', link: '/admin/groups' },
    { title: 'КА',               value: stats.satellites,     icon: <RocketOutlined />, color: '#722ed1', link: null },
    { title: 'Наземные станции', value: stats.groundStations, icon: <WifiOutlined />,   color: '#13c2c2', link: null },
    { title: 'Заявки на съёмку', value: stats.requests,       icon: <CameraOutlined />, color: '#fa8c16', link: null },
  ]

  const userColumns = [
    { title: 'Логин',  dataIndex: 'username', render: (v: string) => <Text strong>{v}</Text> },
    { title: 'Email',  dataIndex: 'email',    render: (v: string) => <Text type="secondary">{v || '—'}</Text> },
    {
      title: 'Роль',
      dataIndex: 'role',
      render: (v: string) => <Tag color={ROLE_COLOR[v] ?? 'default'}>{ROLE_LABEL[v] ?? v}</Tag>,
    },
    {
      title: 'Статус',
      dataIndex: 'is_active',
      render: (v: boolean) => v
        ? <Badge status="success" text="Активен" />
        : <Badge status="error"   text="Неактивен" />,
    },
  ]

  return (
    <div style={{ padding: 24 }}>
      <Title level={4} style={{ marginBottom: 24 }}>Панель администратора</Title>

      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        {statCards.map(sc => (
          <Col key={sc.title} xs={24} sm={12} md={8} lg={6} xl={4}>
            <Card
              hoverable={!!sc.link}
              onClick={() => sc.link && navigate(sc.link)}
              style={{ cursor: sc.link ? 'pointer' : 'default' }}
              bodyStyle={{ padding: '16px 20px' }}
            >
              <Statistic
                title={sc.title}
                value={sc.value}
                prefix={<span style={{ color: sc.color }}>{sc.icon}</span>}
                valueStyle={{ fontSize: 28, fontWeight: 600 }}
              />
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={15}>
          <Card
            title={<><ClockCircleOutlined style={{ marginRight: 8 }} />Последние пользователи</>}
            extra={<a onClick={() => navigate('/admin/users')}>Все →</a>}
          >
            <Table
              rowKey="id"
              dataSource={recentUsers}
              columns={userColumns}
              pagination={false}
              size="small"
            />
          </Card>
        </Col>

        <Col xs={24} lg={9}>
          <Card title={<><TeamOutlined style={{ marginRight: 8 }} />Распределение по ролям</>}>
            {roleStats.length === 0
              ? <Text type="secondary">Нет данных</Text>
              : roleStats.map(rs => (
                  <div key={rs.role} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                    <Tag color={ROLE_COLOR[rs.role] ?? 'default'} style={{ minWidth: 120, textAlign: 'center' }}>
                      {ROLE_LABEL[rs.role] ?? rs.role}
                    </Tag>
                    <Text strong>{rs.count}</Text>
                  </div>
                ))
            }
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default AdminDashboard
