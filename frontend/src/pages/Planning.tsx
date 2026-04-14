import { Card, Button, DatePicker, Select, Form, Row, Col, Table, Tag } from 'antd'
import { PlayCircleOutlined } from '@ant-design/icons'

const { RangePicker } = DatePicker
const { Option } = Select

const Planning = () => {
  const handleForecast = (values: unknown) => {
    console.log('Forecast:', values)
  }

  const handlePlanning = (values: unknown) => {
    console.log('Planning:', values)
  }

  const forecastColumns = [
    { title: 'Название', dataIndex: 'name', key: 'name' },
    { title: 'Период', dataIndex: 'period', key: 'period' },
    { title: 'Статус', dataIndex: 'status', key: 'status', render: (s: string) => <Tag color="blue">{s}</Tag> },
    { title: 'Заявок', dataIndex: 'requests', key: 'requests' },
    { title: 'Окон съёмки', dataIndex: 'opportunities', key: 'opportunities' },
  ]

  const forecastData = [
    { id: 1, name: 'Прогноз на январь', period: '01.01.2024 - 31.01.2024', status: 'Актуальный', requests: 42, opportunities: 156 },
  ]

  return (
    <div>
      <h1 className="page-header">Планирование</h1>
      
      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card title="Прогнозирование">
            <Form layout="vertical" onFinish={handleForecast}>
              <Form.Item name="period" label="Период прогнозирования" rules={[{ required: true }]}>
                <RangePicker style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item name="satellites" label="Космические аппараты">
                <Select mode="multiple" placeholder="Выберите КА">
                  <Option value={1}>КА О-2М-1</Option>
                  <Option value={2}>КА О-2М-2</Option>
                </Select>
              </Form.Item>
              <Button type="primary" icon={<PlayCircleOutlined />} htmlType="submit">
                Запустить прогнозирование
              </Button>
            </Form>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Планирование ПЗ">
            <Form layout="vertical" onFinish={handlePlanning}>
              <Form.Item name="period" label="Период планирования" rules={[{ required: true }]}>
                <RangePicker showTime style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item name="interval" label="Интервал закладки ПЗ (часов)">
                <Select defaultValue={12}>
                  <Option value={6}>6 часов</Option>
                  <Option value={12}>12 часов</Option>
                  <Option value={24}>24 часа</Option>
                </Select>
              </Form.Item>
              <Button type="primary" icon={<PlayCircleOutlined />} htmlType="submit">
                Запустить планирование
              </Button>
            </Form>
          </Card>
        </Col>
      </Row>

      <Card title="Результаты прогнозирования" style={{ marginTop: 24 }}>
        <Table columns={forecastColumns} dataSource={forecastData} rowKey="id" />
      </Card>
    </div>
  )
}

export default Planning
