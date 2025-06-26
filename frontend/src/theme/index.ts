// src/theme/index.ts
import { extendTheme, ThemeConfig } from '@chakra-ui/react';

const config: ThemeConfig = {
  // OS のダークモード設定を初期値に使う
  initialColorMode: 'system',
  useSystemColorMode: true,
};

const styles = {
  global: {
    body: {
      // Light / Dark モードそれぞれの背景・文字色
      bg: 'gray.50',
      color: 'gray.800',
      _dark: {
        bg: 'gray.800',
        color: 'gray.50',
      },
    },
  },
};

const fonts = {
  heading: 'Noto Sans JP, sans-serif',
  body: 'Noto Sans JP, sans-serif',
};

const theme = extendTheme({
  config,
  styles,
  fonts,
});

export default theme;
