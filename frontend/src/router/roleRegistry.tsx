/**
 * РЕЕСТР РОЛЕЙ — единственное место, где описываются роли, их пути и маршруты.
 *
 * Как добавить новую роль:
 *   1. Создать Layout в components/Layout/
 *   2. Создать страницы в pages/<role>/
 *   3. Добавить одну запись в roleRegistry ниже.
 *   Больше нигде ничего трогать не нужно.
 */

import type { ReactNode } from 'react'

// Layouts
import AppLayout    from '../components/Layout/AppLayout'
import AdminLayout  from '../components/Layout/AdminLayout'
// future: import AnalystLayout from '../components/Layout/AnalystLayout'
// future: import ViewerLayout  from '../components/Layout/ViewerLayout'

// Pages — Operator
import Dashboard          from '../pages/Dashboard'
import ImagingRequests    from '../pages/ImagingRequests'
import ImagingRequestEdit from '../pages/ImagingRequestEdit'
import Satellites         from '../pages/Satellites'
import SatelliteDetail    from '../pages/SatelliteDetail'
import GroundStations     from '../pages/GroundStations'
import GroundStationDetail from '../pages/GroundStationDetail'
import Planning           from '../pages/Planning'
import FlightTasks        from '../pages/FlightTasks'

// Pages — Admin
import AdminDashboard from '../pages/admin/AdminDashboard'
import AdminUsers     from '../pages/admin/AdminUsers'
import AdminGroups    from '../pages/admin/AdminGroups'

// ─────────────────────────────────────────────────────────────────────────────

export interface RouteConfig {
  /** Путь относительно basePath. Для индексной страницы оставить пустым ''. */
  path: string
  element: ReactNode
  index?: boolean
}

export interface RoleConfig {
  /** Список ролей, которым разрешён доступ к этому разделу. */
  roles: string[]
  /** Корневой URL-prefix для этой роли. */
  basePath: string
  /** Layout-компонент (обёртка со Sider + Header). */
  Layout: React.ComponentType
  /** Маршруты внутри Layout (вложенные Route). */
  routes: RouteConfig[]
}

/**
 * Главный реестр ролей приложения.
 * Порядок важен: React Router проверяет маршруты сверху вниз.
 */
export const roleRegistry: RoleConfig[] = [
  // ── Администратор ──────────────────────────────────────────────────────────
  {
    roles: ['admin'],
    basePath: '/admin',
    Layout: AdminLayout,
    routes: [
      { path: '',       index: true, element: <AdminDashboard /> },
      { path: 'users',              element: <AdminUsers /> },
      { path: 'groups',             element: <AdminGroups /> },
    ],
  },

  // ── Оператор ───────────────────────────────────────────────────────────────
  {
    roles: ['operator'],
    basePath: '/',
    Layout: AppLayout,
    routes: [
      { path: '',                       index: true, element: <Dashboard /> },
      { path: 'requests',                            element: <ImagingRequests /> },
      { path: 'requests/new',                        element: <ImagingRequestEdit /> },
      { path: 'requests/:id',                        element: <ImagingRequestEdit /> },
      { path: 'satellites',                          element: <Satellites /> },
      { path: 'satellites/:id',                      element: <SatelliteDetail /> },
      { path: 'ground-stations',                     element: <GroundStations /> },
      { path: 'ground-stations/:id',                 element: <GroundStationDetail /> },
      { path: 'planning',                            element: <Planning /> },
      { path: 'flight-tasks',                        element: <FlightTasks /> },
    ],
  },

  // ── Будущие роли (раскомментировать когда будут готовы Layout и страницы) ──
  // {
  //   roles: ['analyst'],
  //   basePath: '/analyst',
  //   Layout: AnalystLayout,
  //   routes: [
  //     { path: '', index: true, element: <AnalystDashboard /> },
  //     { path: 'reports',       element: <AnalystReports /> },
  //   ],
  // },
  // {
  //   roles: ['viewer'],
  //   basePath: '/viewer',
  //   Layout: ViewerLayout,
  //   routes: [
  //     { path: '', index: true, element: <ViewerDashboard /> },
  //   ],
  // },
]

// ─────────────────────────────────────────────────────────────────────────────
// Хелперы

/** Возвращает конфиг роли по строке роли пользователя. */
export function getConfigForRole(role: string): RoleConfig | undefined {
  return roleRegistry.find(cfg => cfg.roles.includes(role))
}

/** Возвращает basePath для роли (для редиректа после логина). */
export function getHomePathForRole(role: string): string {
  return getConfigForRole(role)?.basePath ?? '/'
}
