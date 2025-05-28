import React from 'react';
import { Settings, Key, Database, Bell } from 'lucide-react';

const SettingsPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-2">
          Configure your Deed Reader Pro application
        </p>
      </div>

      <div className="space-y-6">
        {/* API Configuration */}
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <Key className="h-5 w-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">API Configuration</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                OpenAI API Key
              </label>
              <input
                type="password"
                placeholder="sk-..."
                className="input max-w-md"
                disabled
              />
              <p className="text-xs text-gray-500 mt-1">
                Configure your OpenAI API key in the backend environment variables
              </p>
            </div>
          </div>
        </div>

        {/* Processing Settings */}
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <Database className="h-5 w-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Processing Settings</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="rounded border-gray-300 text-primary-600 mr-2" defaultChecked />
                <span className="text-sm text-gray-700">Enable AI-powered analysis</span>
              </label>
            </div>
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="rounded border-gray-300 text-primary-600 mr-2" defaultChecked />
                <span className="text-sm text-gray-700">Auto-analyze uploaded documents</span>
              </label>
            </div>
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="rounded border-gray-300 text-primary-600 mr-2" />
                <span className="text-sm text-gray-700">Save analysis history</span>
              </label>
            </div>
          </div>
        </div>

        {/* Notifications */}
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <Bell className="h-5 w-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">Notifications</h3>
          </div>
          <div className="space-y-4">
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="rounded border-gray-300 text-primary-600 mr-2" defaultChecked />
                <span className="text-sm text-gray-700">Analysis completion notifications</span>
              </label>
            </div>
            <div>
              <label className="flex items-center">
                <input type="checkbox" className="rounded border-gray-300 text-primary-600 mr-2" />
                <span className="text-sm text-gray-700">Error notifications</span>
              </label>
            </div>
          </div>
        </div>

        {/* About */}
        <div className="card">
          <div className="flex items-center gap-3 mb-4">
            <Settings className="h-5 w-5 text-primary-600" />
            <h3 className="text-lg font-semibold text-gray-900">About</h3>
          </div>
          <div className="text-sm text-gray-600">
            <p className="mb-2"><strong>Deed Reader Pro v2.0</strong></p>
            <p className="mb-2">AI-powered deed document analysis for surveyors</p>
            <p>Built with React, TypeScript, and OpenAI API</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage; 