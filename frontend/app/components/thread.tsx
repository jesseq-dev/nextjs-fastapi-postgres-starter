"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import { API_URL } from "../constants";

const Thread = ({ threadId, userId }: { threadId: number; userId: number }) => {
  const [messages, setMessages] = useState<Array<Message>>([]);
  const [input, setInput] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);

  const fetchMessages = async () => {
    try {
      const messages = await fetch(
        `${API_URL}/threads/${threadId}/messages`
      ).then((res) => res.json());

      setMessages(messages);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchMessages();
  }, [threadId]);

  const sendMessage = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    try {
      const data = await fetch(`${API_URL}/thread/messages`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: input,
          sender_id: userId,
          thread_id: threadId,
        }),
      });
      const [message, botMessage] = await data.json();
      setMessages((prevValue) => [...prevValue, message, botMessage]);
      setTimeout(() => {
        if (containerRef.current) {
          containerRef.current.scrollTop = containerRef.current.scrollHeight;
        }
      }, 500);
      setInput("");
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className="flex flex-col h-full justify-between">
      <div
        className="overflow-y-auto"
        style={{ height: "calc(100vh - 120px)" }}
        ref={containerRef}
      >
        <div className="p-8">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.sender_id !== null ? "justify-end" : "justify-start"
              } mb-2`}
            >
              <div
                className={`max-w-xs rounded-lg px-4 py-2 ${
                  message.sender_id !== null
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200 text-gray-800"
                }`}
              >
                {message.content}
              </div>
            </div>
          ))}
        </div>
      </div>
      <form onSubmit={sendMessage}>
        <div className="p-8">
          <input
            className="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            id="message"
            type="text"
            placeholder="Message with Bot"
            required
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        </div>
      </form>
    </div>
  );
};

export default Thread;
