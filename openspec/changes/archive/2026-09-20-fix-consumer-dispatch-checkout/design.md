## Decision

使用固定 SHA 的 checkout action。循环通过 process substitution 在当前 shell 中运行，使汇总失败标志能够成为 job 退出码。
