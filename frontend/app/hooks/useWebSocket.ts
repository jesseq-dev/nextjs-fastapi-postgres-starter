import { useEffect } from "react";
const useWebSocket = (
  url: string,
  threadId: number,
  onMessage: (message: any) => void
) => {
  useEffect(() => {
    const ws = new WebSocket(`${url}/ws/${threadId}`);

    ws.onmessage = async (event) => {
      const text = await event.data.text();
      const message = JSON.parse(text);
      onMessage(message);
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket connection closed");
    };

    return () => {
      ws.close();
    };
  }, [url, threadId, onMessage]);
};

export default useWebSocket;
