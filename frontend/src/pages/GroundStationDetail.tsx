import { useParams } from 'react-router-dom'
import { Card, Descriptions, Tag, Table, Tabs } from 'antd'

const { TabPane } = Tabs

const GroundStationDetail = () => {
  const { id } = useParams()

  const slotColumns = [
    { title: 'Начало', dataIndex: 'start_time', key: 'start_time' },
    { title: 'Конец', dataIndex: 'end_time', key: 'end_time' },
    { title: 'Доступен', dataIndex: 'is_available', key: 'is_available', render: (v: boolean) => v ? <Tag color="green">Да</Tag> : <Tag>Нет</Tag> },
  ]

  const slotData = [
    { id: 1, start_time: '2024-01-15 10:00:00', end_time: '2024-01-15 12:00:00', is_available: true },
    { id: 2, start_time: '2024-01-15 14:00:00', end_time: '2024-01-15 16:00:00', is_available: false },
  ]

  return (
    <div>
      <h1 className="page-header">Карточка НС (ID: {id})</h1>
      
      <Tabs defaultActiveKey="1">
        <TabPane tab="Основная информация" key="1">
          <Card>
            <Descriptions bordered>
              <Descriptions.Item label="Название">ЗСУ Москва</Descriptions.Item>
              <Descriptions.Item label="Код">ZSU-MSK</Descriptions.Item>
              <Descriptions.Item label="Тип">ЗСУ (Земная станция управления)</Descriptions.Item>
              <Descriptions.Item label="Широта">55.7558</Descriptions.Item>
              <Descriptions.Item label="Долгота">37.6173</Descriptions.Item>
              <Descriptions.Item label="Высота">150 м</Descriptions.Item>
              <Descriptions.Item label="Мин. угол возвышения">5°</Descriptions.Item>
              <Descriptions.Item label="Скорость передачи">100 Мбит/с</Descriptions.Item>
              <Descriptions.Item label="Статус"><Tag color="green">Активна</Tag></Descriptions.Item>
            </Descriptions>
          </Card>
        </TabPane>
        <TabPane tab="Слоты связи" key="2">
          <Card>
            <Table columns={slotColumns} dataSource={slotData} rowKey="id" size="small" />
          </Card>
        </TabPane>
        <TabPane tab="Зоны запрета" key="3">
          <Card>
            <p>Зоны запрета отсутствуют</p>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  )
}

export default GroundStationDetail
