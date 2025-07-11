import React from 'react';

export interface Candidate {
  id: string;
  q: string;
  score: number;
}

export function CandidateList({ items, onSelect }: {
  items: Candidate[];
  onSelect: (id: string) => void;
}) {
  return (
    <ul className="space-y-2">
      {items.map((c) => (
        <li
          key={c.id}
          className="cursor-pointer p-2 rounded-lg hover:bg-gray-100"
          onClick={() => onSelect(c.id)}
        >
          {c.q}
        </li>
      ))}
    </ul>
  );
}
