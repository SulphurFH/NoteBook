## 测试

```
go test .
```

## 测试覆盖率

```
go test -coverprofile=c.out
go tool cover -html=c.out
```

## 性能测试

```
go test -bench .
go test -bench . -cpuprofile cpu.out
go tool pprof cpu.out
```
