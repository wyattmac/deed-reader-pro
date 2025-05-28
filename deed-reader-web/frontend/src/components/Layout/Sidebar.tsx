import React from 'react';
import { NavLink } from 'react-router-dom';
import { Home, BarChart3, Map, MessageCircle, Settings, FileText } from 'lucide-react';

const Sidebar: React.FC = () => {
  const navItems = [
    {
      to: '/',
      icon: Home,
      label: 'Home',
      description: 'Upload & start analysis'
    },
    {
      to: '/analysis',
      icon: BarChart3,
      label: 'Analysis',
      description: 'View deed analysis results'
    },
    {
      to: '/plotting',
      icon: Map,
      label: 'Plotting',
      description: 'Interactive deed plotting'
    },
    {
      to: '/chat',
      icon: MessageCircle,
      label: 'Chat',
      description: 'Ask questions about deeds'
    },
    {
      to: '/settings',
      icon: Settings,
      label: 'Settings',
      description: 'Configure application'
    }
  ];

  return (
    <aside className="bg-white w-64 min-h-screen border-r border-gray-200">
      <div className="p-6">
        {/* Logo */}
        <div className="flex items-center space-x-3 mb-8">
          <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
            <FileText className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-gray-900">Deed Reader</h2>
            <p className="text-xs text-gray-500">Professional Edition</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="space-y-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors group ${
                    isActive
                      ? 'bg-primary-50 text-primary-700 border-primary-200'
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    <Icon 
                      size={20} 
                      className={isActive ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600'} 
                    />
                    <div className="flex-1">
                      <div className="text-sm font-medium">{item.label}</div>
                      <div className="text-xs text-gray-500">{item.description}</div>
                    </div>
                  </>
                )}
              </NavLink>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="mt-8 pt-6 border-t border-gray-200">
          <div className="text-xs text-gray-500">
            <p className="font-medium">Deed Reader Pro v2.0</p>
            <p>AI-powered deed analysis</p>
          </div>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar; 