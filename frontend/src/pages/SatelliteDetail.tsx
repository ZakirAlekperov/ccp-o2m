import { useParams } from 'react-router-dom'
import { Card, Descriptions, Tag, Table } from 'antd'

const SatelliteDetail = () => {
  const { id } = useParams()

  const tleColumns = [
    { title: 'Эпоха', dataIndex: 'epoch', key: 'epoch' },
    { title: 'Загружено', dataIndex: 'uploaded_at', key: 'uploaded_at' },
    { title: 'Актуальное', dataIndex: 'is_current', key: 'is_current', render: (v: boolean) => v ? <Tag color="green">Да</Tag> : <Tag>Нет</Tag> },
  ]

  const tleData = [
    { id: 1, epoch: '2024-01-15 12:00:00', uploaded_at: '2024-01-15 10:30:00', is_current: true },
  ]

  return (
    <div>
      <h1 className="page-header">Карточка КА (ID: {id})</h1>
      
      <Card title="Основная информация" style={{ marginBottom: 24 }}>
        <Descriptions bordered>
          <Descriptions.Item label="Название">КА О-2М-1</Descriptions.Item>
          <Descriptions.Item label="NORAD ID">25544</Descriptions.Item>
          <Descriptions.Item label="Статус"><Tag color="green">Активен</Tag></Descriptions.Item>
          <Descriptions.Item label="Полоса захвата">10 км</Descriptions.Item>
          <Descriptions.Item label="Макс. угол крена">30°</Descriptions.Item>
          <Descriptions.Item label="Макс. память">100 ГБ</Descriptions.Item>
          <Descriptions.Item label="Текущая загрузка памяти">45 ГБ (45%)</Descriptions.Item>
        </Descriptions>
      </Card>

      <Card title="TLE данные">
        <Table columns={tleColumns} dataSource={tleData} rowKey="id" size="small" />
      </Card>
    </div>
  )
}

export default SatelliteDetail
