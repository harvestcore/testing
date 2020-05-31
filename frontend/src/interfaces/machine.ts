export interface Machine {
  name: string;
  description?: string;
  type: string;
  ipv4: string;
  ipv6?: string;
  mac?: string;
  broadcast?: string;
  gateway?: string;
  netmask?: string;
  network?: string;
}
