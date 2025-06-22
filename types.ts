// types.ts - Type definitions for the chat monitor

export interface ChatMessage {
  id: string;
  username: string;
  message: string;
  timestamp: string;
  time: Date;
}

export interface ChatStats {
  totalMessages: number;
  todayMessages: number;
  lastMessage: string | null;
}

export interface MonitorError {
  message: string;
  timestamp: Date;
}

export interface ChatMonitorState {
  messages: ChatMessage[];
  isMonitoring: boolean;
  targetUser: string;
  channelName: string;
  stats: ChatStats;
  error: string;
  isLoading: boolean;
}

export interface IframeRef {
  current: HTMLIFrameElement | null;
}

export interface MonitorIntervalRef {
  current: NodeJS.Timeout | null;
}