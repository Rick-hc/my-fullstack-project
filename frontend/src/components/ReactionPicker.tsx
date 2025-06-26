import React from 'react';
import {
  Popover,
  PopoverTrigger,
  PopoverContent,
  HStack,
  IconButton,
} from '@chakra-ui/react';

const emojis = ['👍', '❤️', '😂', '🎉', '😮'];

interface Props {
  onSelect: (emoji: string) => void;
  children: React.ReactElement;
}

const ReactionPicker: React.FC<Props> = ({ onSelect, children }) => (
  <Popover placement="top" trigger="click">
    <PopoverTrigger>{children}</PopoverTrigger>
    <PopoverContent width="auto" p={2}>
      <HStack>
        {emojis.map((e) => (
          <IconButton
            key={e}
            aria-label={e}
            size="sm"
            variant="ghost"
            onClick={() => onSelect(e)}
          >
            {e}
          </IconButton>
        ))}
      </HStack>
    </PopoverContent>
  </Popover>
);

export default ReactionPicker;
