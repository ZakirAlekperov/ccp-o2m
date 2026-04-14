import { useParams } from 'react-router-dom'
import { Card, Form, Input, Select, DatePicker, Button, Row, Col } from 'antd'
import { SaveOutlined } from '@ant-design/icons'

const { TextArea } = Input
const { Option } = Select

const ImagingRequestEdit = () => {
  const { id } = useParams()
  const isEdit = Boolean(id)
  const [form] = Form.useForm()

  const handleSubmit = (values: unknown) => {
    console.log('Submit:', values)
  }

  return (
    <div>
      <h1 className="page-header">
        {isEdit ? 'Редактирование заявки' : 'Создание заявки'}
      </h1>
      <Card>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item
                name="name"
                label="Название"
                rules={[{ required: true, message: 'Введите название' }]}
              >
                <Input placeholder="Название заявки" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item
                name="imaging_type"
                label="Тип съёмки"
                rules={[{ required: true }]}
              >
                <Select placeholder="Выберите тип">
                  <Option value="standard">Стандартная</Option>
                  <Option value="night">Ночная</Option>
                  <Option value="multi_polygon">Мультиполигон</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>

          <Form.Item
            name="description"
            label="Описание"
          >
            <TextArea rows={4} placeholder="Описание заявки" />
          </Form.Item>

          <Row gutter={16}>
            <Col span={8}>
              <Form.Item
                name="priority"
                label="Приоритет (1-10)"
                rules={[{ required: true }]}
              >
                <Select placeholder="Приоритет">
                  {[...Array(10)].map((_, i) => (
                    <Option key={i + 1} value={i + 1}>{i + 1}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="required_resolution"
                label="Требуемое разрешение (м)"
              >
                <Input type="number" placeholder="1.0" />
              </Form.Item>
            </Col>
            <Col span={8}>
              <Form.Item
                name="earliest_start"
                label="Раннее начало"
              >
                <DatePicker showTime style={{ width: '100%' }} />
              </Form.Item>
            </Col>
          </Row>

          <Form.Item>
            <Button type="primary" htmlType="submit" icon={<SaveOutlined />}>
              {isEdit ? 'Сохранить' : 'Создать'}
            </Button>
          </Form.Item>
        </Form>
      </Card>
    </div>
  )
}

export default ImagingRequestEdit
