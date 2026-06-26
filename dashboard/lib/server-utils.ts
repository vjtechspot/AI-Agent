import { RoomServiceClient, SipClient } from 'livekit-server-sdk';

const LIVEKIT_URL = process.env.LIVEKIT_URL || '';
const LIVEKIT_API_KEY = process.env.LIVEKIT_API_KEY || '';
const LIVEKIT_API_SECRET = process.env.LIVEKIT_API_SECRET || '';

export const roomService = LIVEKIT_URL && LIVEKIT_API_KEY && LIVEKIT_API_SECRET 
    ? new RoomServiceClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET) 
    : null;

export const sipClient = LIVEKIT_URL && LIVEKIT_API_KEY && LIVEKIT_API_SECRET 
    ? new SipClient(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET) 
    : null;
