import { Table, Button, Space, Tag } from 'antd'
import { PlusOutlined, EyeOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const Satellites = () => {
  const navigate = useNavigate()

  const columns = [
    {
      title: 'Название',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'NORAD ID',
      dataIndex: 'norad_id',
      key: 'norad_id',
    },
    {
      title: 'Полоса захвата',
      dataIndex: 'swath_width_km',
      key: 'swath_width_km',
      render: (value: number) => `${value} км`,
    },
    {
      title: 'Угол крена',
      dataIndex: 'max_roll_angle',
      key: 'max_roll_angle',
      render: (value: number) => `${value}°`,
    },
    {
      title: 'Статус',
      dataIndex: 'status_display',
      key: 'status',
      render: (status: string) => {
        const colors: Record<string, string> = {
          'Активен': 'green',
          'Неактивен': 'red',
          'Обслуживание': 'orange',
          'Выведен из эксплуатации': 'gray',
        }
        return <Tag color={colors[status] || 'default'}>{status}</Tag>
      },
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_: unknown, record: { id: number }) => (
        <Space>
          <Button type="link" icon={<EyeOutlined />} onClick={() => navigate(`/satellites/${record.id}`)}>
            Просмотр
          </Button>
        </Space>
      ),
    },
  ]

  const data = [
    {
      id: 1,
      name: 'КА О-2М-1',
      norad_id: '25544',
      swath_width_km: 10,
      max_roll_angle: 30,
      status_display: 'Активен',
    },
    {
      id: 2,
      name: 'КА О-2М-2',
      norad_id: '25545',
      swath_width_km: 10,
      max_roll_angle: 30,
      status_display: 'Активен',
    },
  ]

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Космические аппараты</h1>
        <Button type="primary" icon={<PlusOutlined />}>
          Добавить КА
        </Button>
      </div>
      <Table columns={columns} dataSource={data} rowKey="id" />
    </div>
  )
}

export default Satellites
