import { extendTheme } from '@chakra-ui/react';

export default extendTheme({
  styles: {
    global: { body: { bg: 'gray.100', color: 'gray.800' } },
  },
  fonts: {
    heading: 'Noto Sans JP, sans-serif',
    body: 'Noto Sans JP, sans-serif',
  },
});
