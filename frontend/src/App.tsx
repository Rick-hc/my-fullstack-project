import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppLayout from './layouts/AppLayout';
import ChatPage from './pages/ChatPage';
import DocsPage from './pages/DocsPage';
import SettingsPage from './pages/SettingsPage';

const App: React.FC = () => (
  <BrowserRouter>
    <AppLayout>
      <Routes>
        <Route path="/" element={<ChatPage />} />
        <Route path="/docs" element={<DocsPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Routes>
    </AppLayout>
  </BrowserRouter>
);

export default App;
