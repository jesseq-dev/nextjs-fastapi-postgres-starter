type User = {
    id: number;
    name: string;
  };
  
  type Thread = {
    id: number;
    created_by: number;
    created_at: Date;
    updated_at: Date;
  };
  
  type Message = {
    id: number;
    content: string;
    sender_id: number | null;
    thread_id: number;
    created_at: Date;
  };