import { useEffect, useState } from 'react'
import { Row, Col, Card, Statistic, Typography, Spin, Alert } from 'antd'
import { UserOutlined, TeamOutlined } from '@ant-design/icons'
import { useSelector } from 'react-redux'
import type { RootState } from '../../store'

const { Title } = Typography

const API_URL = '/api'

const AdminDashboard = () => {
  const { token } = useSelector((state: RootState) => state.auth)
  const [stats, setStats] = useState({ total_users: 0, total_groups: 0 })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [usersRes, groupsRes] = await Promise.all([
          fetch(`${API_URL}/auth/users/`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`${API_URL}/auth/groups/`, { headers: { Authorization: `Bearer ${token}` } }),
        ])
        if (!usersRes.ok || !groupsRes.ok) throw new Error('Ошибка загрузки данных')
        const users = await usersRes.json()
        const groups = await groupsRes.json()
        setStats({
          total_users: Array.isArray(users) ? users.length : (users.count ?? 0),
          total_groups: Array.isArray(groups) ? groups.length : (groups.count ?? 0),
        })
      } catch (e: any) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    fetchStats()
  }, [token])

  if (loading) return <Spin size="large" style={{ display: 'block', marginTop: 80, textAlign: 'center' }} />
  if (error) return <Alert type="error" message={error} style={{ margin: 24 }} />

  return (
    <div style={{ padding: 24 }}>
      <Title level={3}>Панель администратора</Title>
      <Row gutter={16}>
        <Col span={8}>
          <Card>
            <Statistic title="Всего пользователей" value={stats.total_users} prefix={<UserOutlined />} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="Группы" value={stats.total_groups} prefix={<TeamOutlined />} />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default AdminDashboard
