import { NextResponse } from 'next/server';
import { sipClient } from '@/lib/server-utils';

export async function POST(request: Request) {
    try {
        const body = await request.json();
        const { phoneNumber, prompt, modelProvider, voice } = body;

        if (!phoneNumber) {
            return NextResponse.json({ error: "Phone number is required" }, { status: 400 });
        }

        if (!sipClient) {
            return NextResponse.json({ error: "LiveKit credentials not configured" }, { status: 500 });
        }

        const trunkId = process.env.VOBIZ_SIP_TRUNK_ID;
        if (!trunkId) {
            console.error("VOBIZ_SIP_TRUNK_ID is missing in env");
            return NextResponse.json({ error: "SIP Trunk not configured" }, { status: 500 });
        }

        // Generate a unique room name for this call
        const roomName = `call-${phoneNumber.replace(/\+/g, '')}-${Math.floor(Math.random() * 10000)}`;
        const particpantIdentity = `sip_${phoneNumber}`;

        console.log(`Dispatching call to ${phoneNumber} in room ${roomName} via trunk ${trunkId}`);

        const metadata = JSON.stringify({
            phone_number: phoneNumber,
            user_prompt: prompt || "",
            model_provider: modelProvider || "openai",
            voice_id: voice || "alloy"
        });

        const info = await sipClient.createSipParticipant(
            trunkId,
            phoneNumber,
            roomName,
            {
                participantIdentity: particpantIdentity,
                participantName: "Customer",
                participantMetadata: metadata,
            }
        );

        return NextResponse.json({
            success: true,
            roomName,
            dispatchId: info.sipCallId
        });

    } catch (error: any) {
        console.error("Error dispatching call:", error);
        return NextResponse.json({ error: error.message || "Internal Server Error" }, { status: 500 });
    }
}
