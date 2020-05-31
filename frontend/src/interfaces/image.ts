export interface Image {
  id: string;
  labels: any;
  short_id: string;
  tags: string;
}

export interface SingleImageOperation {
  name: string;
  operation: string;
  data: any;
}

export interface ImageOperation {
  operation: string;
  data: any;
}
