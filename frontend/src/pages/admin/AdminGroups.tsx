import { Typography, Card, Tag, Row, Col, Table, Badge } from 'antd'
import { TeamOutlined, LockOutlined } from '@ant-design/icons'
import type { ColumnsType } from 'antd/es/table'

const { Title, Text, Paragraph } = Typography

const ROLES = [
  {
    key: 'admin',
    label: 'Администратор',
    color: 'red',
    description: 'Полный доступ к системе. Управление пользователями, всеми объектами и данными.',
    permissions: [
      { name: 'Управление пользователями', granted: true },
      { name: 'Управление КА и станциями', granted: true },
      { name: 'Создание заявок на съёмку', granted: true },
      { name: 'Планирование',              granted: true },
      { name: 'Экспорт данных',            granted: true },
      { name: 'Просмотр данных',           granted: true },
    ],
  },
  {
    key: 'operator',
    label: 'Оператор',
    color: 'blue',
    description: 'Работа с КА, наземными станциями, заявками на съёмку и планированием.',
    permissions: [
      { name: 'Управление пользователями', granted: false },
      { name: 'Управление КА и станциями', granted: true },
      { name: 'Создание заявок на съёмку', granted: true },
      { name: 'Планирование',              granted: true },
      { name: 'Экспорт данных',            granted: false },
      { name: 'Просмотр данных',           granted: true },
    ],
  },
  {
    key: 'analyst',
    label: 'Аналитик',
    color: 'purple',
    description: 'Просмотр данных, создание заявок на съёмку и экспорт данных для анализа.',
    permissions: [
      { name: 'Управление пользователями', granted: false },
      { name: 'Управление КА и станциями', granted: false },
      { name: 'Создание заявок на съёмку', granted: true },
      { name: 'Планирование',              granted: false },
      { name: 'Экспорт данных',            granted: true },
      { name: 'Просмотр данных',           granted: true },
    ],
  },
  {
    key: 'viewer',
    label: 'Наблюдатель',
    color: 'default',
    description: 'Только просмотр данных. Изменение объектов недоступно.',
    permissions: [
      { name: 'Управление пользователями', granted: false },
      { name: 'Управление КА и станциями', granted: false },
      { name: 'Создание заявок на съёмку', granted: false },
      { name: 'Планирование',              granted: false },
      { name: 'Экспорт данных',            granted: false },
      { name: 'Просмотр данных',           granted: true },
    ],
  },
]

const permColumns: ColumnsType<{ name: string; granted: boolean }> = [
  {
    title: 'Разрешение',
    dataIndex: 'name',
    render: (v) => <Text>{v}</Text>,
  },
  {
    title: 'Доступ',
    dataIndex: 'granted',
    width: 100,
    render: (v) => v
      ? <Badge status="success" text={<Text type="success">Да</Text>} />
      : <Badge status="default" text={<Text type="secondary">Нет</Text>} />,
  },
]

const AdminGroups = () => (
  <div style={{ padding: 24 }}>
    <div style={{ marginBottom: 24 }}>
      <Title level={4} style={{ marginBottom: 4 }}>Группы и роли</Title>
      <Paragraph type="secondary" style={{ marginBottom: 0 }}>
        Роли определяются на уровне системы. Каждому пользователю назначается одна роль в разделе{' '}
        <a href="/admin/users">«Пользователи»</a>.
      </Paragraph>
    </div>

    <Row gutter={[16, 16]}>
      {ROLES.map(role => (
        <Col key={role.key} xs={24} md={12}>
          <Card
            title={
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <TeamOutlined />
                <Tag color={role.color} style={{ marginBottom: 0 }}>{role.label}</Tag>
              </div>
            }
          >
            <Paragraph type="secondary" style={{ marginBottom: 16 }}>
              {role.description}
            </Paragraph>
            <Table
              rowKey="name"
              dataSource={role.permissions}
              columns={permColumns}
              pagination={false}
              size="small"
              showHeader={false}
            />
          </Card>
        </Col>
      ))}
    </Row>

    <Card style={{ marginTop: 16 }}>
      <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start' }}>
        <LockOutlined style={{ marginTop: 3, color: '#8c8c8c' }} />
        <Paragraph type="secondary" style={{ marginBottom: 0 }}>
          Роли и их права зафиксированы в модели <Text code>UserRole</Text> на бэкенде.
          Чтобы добавить новую роль — добавь значение в <Text code>users/models.py</Text>,
          затем раскомментируй заготовку в <Text code>frontend/src/router/roleRegistry.tsx</Text>.
        </Paragraph>
      </div>
    </Card>
  </div>
)

export default AdminGroups
