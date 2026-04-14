import { Table, Button, Space, Tag } from 'antd'
import { PlusOutlined, EyeOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const GroundStations = () => {
  const navigate = useNavigate()

  const columns = [
    {
      title: 'Название',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Код',
      dataIndex: 'code',
      key: 'code',
    },
    {
      title: 'Тип',
      dataIndex: 'station_type_display',
      key: 'station_type',
    },
    {
      title: 'Координаты',
      key: 'coordinates',
      render: (_: unknown, record: { latitude: number; longitude: number }) => 
        `${record.latitude}, ${record.longitude}`,
    },
    {
      title: 'Статус',
      dataIndex: 'status_display',
      key: 'status',
      render: (status: string) => {
        const colors: Record<string, string> = {
          'Активна': 'green',
          'Неактивна': 'red',
          'Обслуживание': 'orange',
        }
        return <Tag color={colors[status] || 'default'}>{status}</Tag>
      },
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_: unknown, record: { id: number }) => (
        <Space>
          <Button type="link" icon={<EyeOutlined />} onClick={() => navigate(`/ground-stations/${record.id}`)}>
            Просмотр
          </Button>
        </Space>
      ),
    },
  ]

  const data = [
    {
      id: 1,
      name: 'ЗСУ Москва',
      code: 'ZSU-MSK',
      station_type_display: 'ЗСУ (Земная станция управления)',
      latitude: 55.7558,
      longitude: 37.6173,
      status_display: 'Активна',
    },
    {
      id: 2,
      name: 'ЗС ПД Новосибирск',
      code: 'ZSPD-NSK',
      station_type_display: 'ЗС ПД (Земная станция приёма данных)',
      latitude: 55.0084,
      longitude: 82.9357,
      status_display: 'Активна',
    },
  ]

  return (
    <div>
      <div className="page-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Наземные станции</h1>
        <Button type="primary" icon={<PlusOutlined />}>
          Добавить станцию
        </Button>
      </div>
      <Table columns={columns} dataSource={data} rowKey="id" />
    </div>
  )
}

export default GroundStations
