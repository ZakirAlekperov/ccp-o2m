import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import type { RootState } from './store'
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
import Login from './pages/Login'
import './App.css'

// Защищённый роут — редиректит на /login если нет токена
const PrivateRoute = ({ children }: { children: React.ReactNode }) => {
  const { token } = useSelector((state: RootState) => state.auth)
  return token ? <>{children}</> : <Navigate to="/login" replace />
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
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
        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
