### 使用参考链接
https://hpc-cool.feishu.cn/docx/WtUod0MIbowDYJxOpcgc9kuanod
https://zhuanlan.zhihu.com/p/360479566

### 使用方法
```python
with torch.autograd.profiler.profile(enabled=True, use_cuda=True, record_shapes=False, profile_memory=False) as prof:
    # 被测部分，即使只有一行torch.rand(3,3),也是可以被测量
#输出结果
#输出原始内容
print(prof.table())
#输出排序结果
print(prof.key_averages().table(sort_by="self_cpu_time_total", row_limit=100))
```

### 使用结果示例
```bash
STAGE:2023-06-10 11:46:02 11920:11920 ActivityProfilerController.cpp:317] Completed Stage: Collection
STAGE:2023-06-10 11:46:02 11920:11920 ActivityProfilerController.cpp:321] Completed Stage: Post Processing
-------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  
                                       Name    Self CPU %      Self CPU   CPU total %     CPU total  CPU time avg    # of Calls  
-------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  
                             aten::uniform_        65.86%     102.130ms        65.86%     102.130ms       4.642ms            22  
                              aten::normal_        31.82%      49.343ms        31.82%      49.343ms       2.467ms            20  
                                aten::fill_         1.44%       2.233ms         1.44%       2.233ms      22.109us           101  
                                aten::empty         0.39%     597.000us         0.39%     597.000us       4.854us           123  
                                     detach         0.15%     238.000us         0.15%     238.000us       3.839us            62  
                               aten::detach         0.08%     129.000us         0.22%     334.000us       5.387us            62  
                                 aten::ones         0.08%     127.000us         1.44%       2.230ms     106.190us            21  
                                aten::zeros         0.07%     110.000us         0.10%     150.000us       7.500us            20  
                                aten::zero_         0.06%      90.000us         0.06%      90.000us       1.125us            80  
                              aten::detach_         0.02%      24.000us         0.02%      31.000us       1.550us            20  
                                   aten::to         0.01%      20.000us         0.01%      20.000us       0.140us           143  
                                    detach_         0.01%       9.000us         0.01%       9.000us       0.450us            20  
                           aten::lift_fresh         0.00%       7.000us         0.00%       7.000us       0.350us            20  
    aten::_has_compatible_shallow_copy_type         0.00%       4.000us         0.00%       4.000us       0.032us           124  
-------------------------------------------  ------------  ------------  ------------  ------------  ------------  ------------  
Self CPU time total: 155.061ms
```