"use client";

import { useEffect, useState } from "react";
import ChatThread from "./components/thread";
import { API_URL } from "./constants";
import LoadingSpinner from "./components/loading";

export default function Home() {
  const [user, setUser] = useState<null | User>(null);
  const [threads, setThreads] = useState<Array<Thread>>([]);
  const [selectedThread, setSelectedThread] = useState<Thread | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchUser = async () => {
    const user: User = await fetch(`${API_URL}/users/me`).then((res) =>
      res.json()
    );

    return user;
  };

  const fetchThreads = async () => {
    const threads: Thread[] = await fetch(`${API_URL}/threads`).then((res) =>
      res.json()
    );

    return threads;
  };

  useEffect(() => {
    setLoading(true);
    Promise.all([fetchUser(), fetchThreads()])
      .then(([user, threads]) => {
        setUser(user);
        setThreads(threads);
        setSelectedThread(threads[0] || null);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!threads.length) {
    return null;
  }

  return (
    <main className="flex flex-col items-center min-h-screen">
      <div className="flex flex-row w-full min-h-screen">
        <div className="flex flex-col bg-gray-900 p-4" style={{ width: 350 }}>
          <h1 className="font-bold text-white mb-4">Chat History</h1>
          {threads.length !== 0 &&
            threads.map((thread) => {
              return (
                <div
                  key={thread.id}
                  onClick={() => setSelectedThread(thread)}
                  className={`flex justify-center items-center shadow-md rounded px-8 pt-6 pb-8 cursor-pointer text-white
                    ${
                      selectedThread?.id === thread.id
                        ? "bg-blue-200 hover:bg-blue-100"
                        : "bg-white hover:bg-gray-100"
                    }`}
                >
                  Thread #{thread.id}
                </div>
              );
            })}
        </div>
        {selectedThread && user && (
          <div className="shadow-md rounded bg-gray-400 w-full">
            <ChatThread threadId={selectedThread.id} userId={user.id} />
          </div>
        )}
      </div>
    </main>
  );
}
