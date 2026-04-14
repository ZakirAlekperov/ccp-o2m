import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import type { RootState } from './store'

// Operator (основной) layout
import AppLayout from './components/Layout/AppLayout'
import Dashboard from './pages/Dashboard'
import ImagingRequests from './pages/ImagingRequests'
import ImagingRequestEdit from './pages/ImagingRequestEdit'
import Satellites from './pages/Satellites'
import SatelliteDetail from './pages/SatelliteDetail'
import GroundStations from './pages/GroundStations'
import GroundStationDetail from './pages/GroundStationDetail'
import Planning from './pages/Planning'
import FlightTasks from './pages/FlightTasks'

// Admin layout
import AdminLayout from './components/Layout/AdminLayout'
import AdminDashboard from './pages/admin/AdminDashboard'
import AdminUsers from './pages/admin/AdminUsers'
import AdminGroups from './pages/admin/AdminGroups'

import Login from './pages/Login'
import './App.css'

// Защищённый роут — редиректит на /login если нет токена
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { token } = useSelector((state: RootState) => state.auth)
  return token ? <>{children}</> : <Navigate to="/login" replace />
}

// Роут только для администратора
const AdminRoute = ({ children }: { children: React.ReactNode }) => {
  const { token, user } = useSelector((state: RootState) => state.auth)
  if (!token) return <Navigate to="/login" replace />
  if (user?.role !== 'admin') return <Navigate to="/" replace />
  return <>{children}</>
}

// Роутинг зависит от роли пользователя.
// Добавление новой роли: создать RoleRoute и новый Layout + страницы,
// затем добавить секцию <Route path="/role-name/*" ...> ниже.
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />

        {/* === Оператор === */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <AppLayout />
            </PrivateRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="requests" element={<ImagingRequests />} />
          <Route path="requests/new" element={<ImagingRequestEdit />} />
          <Route path="requests/:id" element={<ImagingRequestEdit />} />
          <Route path="satellites" element={<Satellites />} />
          <Route path="satellites/:id" element={<SatelliteDetail />} />
          <Route path="ground-stations" element={<GroundStations />} />
          <Route path="ground-stations/:id" element={<GroundStationDetail />} />
          <Route path="planning" element={<Planning />} />
          <Route path="flight-tasks" element={<FlightTasks />} />
        </Route>

        {/* === Администратор === */}
        <Route
          path="/admin"
          element={
            <AdminRoute>
              <AdminLayout />
            </AdminRoute>
          }
        >
          <Route index element={<AdminDashboard />} />
          <Route path="users" element={<AdminUsers />} />
          <Route path="groups" element={<AdminGroups />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
