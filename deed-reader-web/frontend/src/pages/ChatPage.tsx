import React from 'react';
import { MessageCircle, Upload } from 'lucide-react';

const ChatPage: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="card text-center py-12">
        <MessageCircle className="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h2 className="text-xl font-semibold text-gray-900 mb-2">
          Interactive Chat Coming Soon
        </h2>
        <p className="text-gray-600 mb-6">
          Ask questions about your deed documents and get instant AI-powered answers.
        </p>
        <button className="btn-primary">
          <Upload size={16} />
          Upload Document to Start Chatting
        </button>
      </div>
    </div>
  );
};

export default ChatPage; 