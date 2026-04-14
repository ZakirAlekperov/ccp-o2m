/**
 * RoleRoute — универсальный guard для защищённых маршрутов.
 *
 * Логика:
 *   1. Нет токена → /login
 *   2. Роль пользователя не входит в allowedRoles → редирект на его "домашнюю" страницу
 *   3. Всё ок → рендерим children
 */

import { Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import type { RootState } from '../store'
import { getHomePathForRole } from './roleRegistry'

interface RoleRouteProps {
  allowedRoles: string[]
  children: React.ReactNode
}

const RoleRoute = ({ allowedRoles, children }: RoleRouteProps) => {
  const { token, user } = useSelector((state: RootState) => state.auth)

  // Не авторизован
  if (!token) return <Navigate to="/login" replace />

  const role = user?.role ?? ''

  // Авторизован, но роль не подходит → отправляем на его страницу
  if (!allowedRoles.includes(role)) {
    return <Navigate to={getHomePathForRole(role)} replace />
  }

  return <>{children}</>
}

export default RoleRoute
