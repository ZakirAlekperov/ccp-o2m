import { Card, Row, Col, Statistic } from 'antd'
import { CameraOutlined, RocketOutlined, CalendarOutlined, FileTextOutlined } from '@ant-design/icons'

const Dashboard = () => {
  return (
    <div>
      <h1 className="page-header">Главная панель</h1>
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Заявок на съёмку"
              value={42}
              prefix={<CameraOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Космических аппаратов"
              value={6}
              prefix={<RocketOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Запланировано съёмок"
              value={128}
              prefix={<CalendarOutlined />}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card>
            <Statistic
              title="Полётных заданий"
              value={15}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Dashboard
