export interface User {
  type: string;
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  public_id?: string;
  password?: string;
}
