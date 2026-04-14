import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import RoleRoute from './router/RoleRoute'
import { roleRegistry } from './router/roleRegistry'
import './App.css'

/**
 * App.tsx намеренно простой — вся логика ролей живёт в roleRegistry.
 * Чтобы добавить новую роль, трогать этот файл не нужно.
 */
function App() {
  return (
    <Router>
      <Routes>
        {/* Публичный маршрут */}
        <Route path="/login" element={<Login />} />

        {/* Защищённые маршруты — генерируются из реестра ролей */}
        {roleRegistry.map(cfg => (
          <Route
            key={cfg.basePath}
            path={cfg.basePath === '/' ? '/' : `${cfg.basePath}/*`}
            element={
              <RoleRoute allowedRoles={cfg.roles}>
                <cfg.Layout />
              </RoleRoute>
            }
          >
            {cfg.routes.map(route =>
              route.index
                ? <Route key="_index" index element={route.element} />
                : <Route key={route.path} path={route.path} element={route.element} />
            )}
          </Route>
        ))}

        {/* Fallback — на корень, RoleRoute сам разберётся куда редиректить */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  )
}

export default App
