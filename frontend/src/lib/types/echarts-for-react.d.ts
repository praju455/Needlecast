declare module "echarts-for-react" {
  import type { ComponentType, CSSProperties } from "react";
  const ECharts: ComponentType<{ option: object; style?: CSSProperties; notMerge?: boolean }>;
  export default ECharts;
}
