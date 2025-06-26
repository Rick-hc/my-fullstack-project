import React from 'react';
import { Box } from '@chakra-ui/react';
import Header from '../components/Header';

const AppLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <Box display="flex" flexDir="column" h="100vh">
    <Header />
    <Box display="flex" flex="1">
      <aside style={{ width: 240, background: '#f5f5f5', padding: 16 }}>
        Sidebar
      </aside>
      <main style={{ flex: 1, padding: 16 }}>{children}</main>
    </Box>
  </Box>
);

export default AppLayout;
