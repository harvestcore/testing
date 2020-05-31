export interface Container {
  id: string;
  labels: any;
  name: string;
  short_id: string;
  status: string;
}

export interface SingleContainerOperation {
  container_id: string;
  operation: string;
  data: any;
}

export interface ContainerOperation {
  operation: string;
  data: any;
}
