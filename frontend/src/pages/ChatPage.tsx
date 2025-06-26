import React from 'react';
import { Box, Flex, Heading, useColorModeValue } from '@chakra-ui/react';
import ChatWindow from '../components/ChatWindow';

/**
 * ChatPage – content‑only.
 * Header / Sidebar は AppLayout が描画するため、ここでは不要。
 */
const ChatPage: React.FC = () => {
  const bg = useColorModeValue('gray.50', 'gray.900');

  return (
    <Flex direction="column" h="100vh" bg={bg}>
      <Box as="main" id="main" flex="1" overflow="hidden">
        <Flex direction="column" h="full" maxW="4xl" mx="auto">
          <Heading
            as="h2"
            size="md"
            px={{ base: 4, md: 6 }}
            pt={4}
            pb={2}
            color={useColorModeValue('gray.700', 'gray.200')}
          >
            歯科チャットボット
          </Heading>

          {/* Chat UI */}
          <ChatWindow />
        </Flex>
      </Box>
    </Flex>
  );
};

export default ChatPage;
