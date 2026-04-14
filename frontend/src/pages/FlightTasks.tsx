import { Table, Button, Space, Tag } from 'antd'
import { ExportOutlined, EyeOutlined } from '@ant-design/icons'

const FlightTasks = () => {
  const columns = [
    {
      title: 'Номер группы',
      dataIndex: 'group_number',
      key: 'group_number',
    },
    {
      title: 'Название',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Период',
      dataIndex: 'period',
      key: 'period',
    },
    {
      title: 'Статус',
      dataIndex: 'status_display',
      key: 'status',
      render: (status: string) => {
        const colors: Record<string, string> = {
          'Новое': 'blue',
          'Согласование': 'orange',
          'Отправлено': 'cyan',
          'Одобрено': 'green',
          'Выполняется': 'purple',
          'Выполнено': 'green',
        }
        return <Tag color={colors[status] || 'default'}>{status}</Tag>
      },
    },
    {
      title: 'ПЗ',
      dataIndex: 'total_tasks',
      key: 'total_tasks',
    },
    {
      title: 'Действия',
      key: 'actions',
      render: () => (
        <Space>
          <Button type="link" icon={<EyeOutlined />}>Просмотр</Button>
          <Button type="link" icon={<ExportOutlined />}>Экспорт</Button>
        </Space>
      ),
    },
  ]

  const data = [
    {
      id: 1,
      group_number: 'PZ-20240115-001',
      name: 'План на 15-17 января',
      period: '15.01.2024 00:00 - 17.01.2024 00:00',
      status_display: 'Одобрено',
      total_tasks: 24,
    },
    {
      id: 2,
      group_number: 'PZ-20240117-002',
      name: 'План на 17-19 января',
      period: '17.01.2024 00:00 - 19.01.2024 00:00',
      status_display: 'Согласование',
      total_tasks: 18,
    },
  ]

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Полётные задания</h1>
        <Button type="primary" icon={<ExportOutlined />}>
          Экспорт в КУП
        </Button>
      </div>
      <Table columns={columns} dataSource={data} rowKey="id" />
    </div>
  )
}

export default FlightTasks
