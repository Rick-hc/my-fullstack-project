// src/components/DarkModeSwitch.tsx
import React, { useEffect, useState } from 'react';
import { IconButton, useColorMode } from '@chakra-ui/react';
import { FiMoon, FiSun } from 'react-icons/fi';

export const DarkModeSwitch: React.FC = () => {
  const { colorMode, toggleColorMode } = useColorMode();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  if (!mounted) return null;

  return (
    <IconButton
      aria-label="ダークモード切替"
      onClick={toggleColorMode}
      variant="ghost"
      size="lg"
      icon={colorMode === 'light' ? <FiMoon /> : <FiSun />}
    />
  );
};
