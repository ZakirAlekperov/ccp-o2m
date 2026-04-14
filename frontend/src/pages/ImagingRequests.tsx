import { Table, Button, Space, Tag, Input } from 'antd'
import { PlusOutlined, SearchOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const ImagingRequests = () => {
  const navigate = useNavigate()

  const columns = [
    {
      title: 'Номер',
      dataIndex: 'request_number',
      key: 'request_number',
    },
    {
      title: 'Название',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Тип',
      dataIndex: 'imaging_type_display',
      key: 'imaging_type',
    },
    {
      title: 'Приоритет',
      dataIndex: 'priority',
      key: 'priority',
    },
    {
      title: 'Статус',
      dataIndex: 'status_display',
      key: 'status',
      render: (status: string) => {
        const colors: Record<string, string> = {
          'Новая': 'blue',
          'Согласована': 'green',
          'Выполняется': 'orange',
          'Завершена': 'green',
          'Отменена': 'red',
        }
        return <Tag color={colors[status] || 'default'}>{status}</Tag>
      },
    },
    {
      title: 'Создана',
      dataIndex: 'created_at',
      key: 'created_at',
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_: unknown, record: { id: number }) => (
        <Space>
          <Button type="link" onClick={() => navigate(`/requests/${record.id}`)}>
            Редактировать
          </Button>
        </Space>
      ),
    },
  ]

  const data = [
    {
      id: 1,
      request_number: 'REQ-20240115-A1B2C3',
      name: 'Съёмка Московской области',
      imaging_type_display: 'Стандартная',
      priority: 8,
      status_display: 'Новая',
      created_at: '2024-01-15 10:30:00',
    },
    {
      id: 2,
      request_number: 'REQ-20240114-D4E5F6',
      name: 'Съёмка Санкт-Петербурга',
      imaging_type_display: 'Ночная',
      priority: 5,
      status_display: 'Согласована',
      created_at: '2024-01-14 14:20:00',
    },
  ]

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Заявки на съёмку</h1>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => navigate('/requests/new')}>
          Создать заявку
        </Button>
      </div>
      <div style={{ marginBottom: 16 }}>
        <Input.Search
          placeholder="Поиск заявок"
          enterButton={<SearchOutlined />}
          style={{ width: 300 }}
        />
      </div>
      <Table columns={columns} dataSource={data} rowKey="id" />
    </div>
  )
}

export default ImagingRequests
