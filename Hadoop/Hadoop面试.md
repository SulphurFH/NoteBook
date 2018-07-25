1.请说说hadoop1的HA如何实现？

```
hadoop1.x之前的namenode存在两个主要的问题：1、namenode内存瓶颈的问题，2、namenode的单点故障的问题。针对这两个问题，hadoop2.x都对它进行改进和解决。其中，问题1中对namenode内存瓶颈的问题采用扩展namenode的方式来解决。对于问题2中的namenode的单点故障问题hadoop2.x采用的是HA的解决方案。apache hadoop 官方网站上提供了两种解决HDFS High Availability Using the Quorum Journal Manager 和High Availability with NFS
```

2.列举出hadoop中定义的最常用的InputFormats。那个是默认的？

```
TextInputFormat
```



3.请列出正常工作的Hadoop集群中Hadoop都分别需要启动哪些进程，它们的作用分别是什么?

```
a) NameNode它是hadoop中的主服务器，管理文件系统名称空间和对集群中存储的文件的访问，保存有 metadate.

b).SecondaryNameNode它不是namenode的冗余守护进程，而是提供周期检查点和清理任务。帮助NN合并editslog，减少NN启动时间。

c)DataNode它负责管理连接到节点的存储(一个集群中可以有多个节点)。每个存储数据的节点运行一个datanode守护进程。

d)ResourceManager(JobTracker)JobTracker负责调度DataNode上的工作。每个DataNode有一个TaskTracker，它们执行实际工作。

e) NodeManager(TaskTracker)执行任务

f) DFSZKFailoverController高可用时它负责监控NN的状态，并及时的把状态信息写入ZK。它通过一个独立线程周期性的调用NN上的一个特定接口来获取NN的健康状态。FC也有选择谁作为Active NN的权利，因为最多只有两个节点，目前选择策略还比较简单(先到先得，轮换)。

g) JournalNode 高可用情况下存放namenode的editlog文件.
```

4.hadoop中的InputSplit是什么？

```
1、运行mapred程序；
2、本次运行将生成一个Job，于是JobClient向JobTracker申请一个JobID以标识这个Job；
3、JobClient将Job所需要的资源提交到HDFS中一个以JobID命名的目录中。这些资源包括JAR包、配置文件、InputSplit、等；
4、JobClient向JobTracker提交这个Job；
5、JobTracker初始化这个Job；
6、JobTracker从HDFS获取这个Job的Split等信息；
7、JobTracker向TaskTracker分配任务；
8、TaskTracker从HDFS获取这个Job的相关资源；
9、TaskTracker开启一个新的JVM；
10、TaskTracker用新的JVM来执行Map或Reduce；

InputSplit是指分片，在MapReduce作业中，作为map task最小输入单位。分片是基于文件基础上出来的概念，通俗的理解一个文件可以切分为多少个片段，每个片段包括了<文件名，开始位置，长度，位于哪些主机>等信息。在    MapTask    拿到这些分片后，会知道从哪开始读取数据。
```

5.hadoop中job和task之间是什么关系

```
Jobtracker最重要的功能之一是状态监控，包括tasktracker、job、task等运行时状态的监控，Tasktracker监控比较简单，只要记录其最近心跳汇报时间和健康状态就可以了
```

12.关系型数据库有什么弱点？

```
很难进行分布式部署，I/O瓶颈显著，依赖于强大的服务器，需要花更大的代价才能突破性能极限
很难处理非结构化数据
```

13.什么情况下使用hbase？

```
适合海量的，但同时也是简单的操作（例如：key-value）
成熟的数据分析主题，查询模式已经确定并且不会轻易改变。
传统的关系型数据库已经无法承受负荷，高速插入，大量读取
```

为什么会产生yarn, 它解决了什么问题，有什么优势？

```
MapReduce 的第一个版本既有优点也有缺点。MRv1 是目前使用的标准的大数据处理系统。但是，这种架构存在不足，主要表现在大型集群上。当集群包含的节点超过 4,000 个时（其中每个节点可能是多核的），就会表现出一定的不可预测性。其中一个最大的问题是级联故障，由于要尝试复制数据和重载活动的节点，所以一个故障会通过网络泛洪形式导致整个集群严重恶化

YARN 分层结构的本质是 ResourceManager。这个实体控制整个集群并管理应用程序向基础计算资源的分配。ResourceManager 将各个资源部分（计算、内存、带宽等）精心安排给基础 NodeManager（YARN 的每节点代理）。ResourceManager 还与 ApplicationMaster 一起分配资源，与 NodeManager 一起启动和监视它们的基础应用程序。在此上下文中，ApplicationMaster 承担了以前的 TaskTracker 的一些角色，ResourceManager 承担了 JobTracker 的角色。
```

对于MapReduce作业，完整的作业运行流程

```
完整过程应该是分为7部分，分别是：

作业启动：开发者通过控制台启动作业；
作业初始化：这里主要是切分数据、创建作业和提交作业，与第三步紧密相联；
作业/任务调度：对于1.0版的Hadoop来说就是JobTracker来负责任务调度，对于2.0版的Hadoop来说就是Yarn中的Resource Manager负责整个系统的资源管理与分配，Yarn可以参考IBM的一篇博客Hadoop新MapReduce框架Yarn详解；
Map任务；
Shuffle；
Reduce任务；
作业完成：通知开发者任务完成。

而这其中最主要的MapReduce过程，主要是第4、5、6步三部分，这也是本篇博客重点讨论的地方，详细作用如下：

Map:数据输入,做初步的处理,输出形式的中间结果；
Shuffle:按照partition、key对中间结果进行排序合并,输出给reduce线程；
Reduce:对相同key的输入进行最终的处理,并将结果写入到文件中。
```


Top K 问题

```
package seven.ili.patent;

/**
 * Created with IntelliJ IDEA.
 * User: Isaac Li
 * Date: 12/4/12
 * Time: 5:48 PM
 * To change this template use File | Settings | File Templates.
 */

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;
import java.util.TreeMap;

//利用MapReduce求最大值海量数据中的K个数
public class Top_k_new extends Configured implements Tool {

    public static class MapClass extends Mapper<LongWritable, Text, NullWritable, Text> {
        public static final int K = 100;
        private TreeMap<Integer, Text> fatcats = new TreeMap<Integer, Text>();
        public void map(LongWritable key, Text value, Context context)
                throws IOException, InterruptedException {

            String[] str = value.toString().split(",", -2);
            int temp = Integer.parseInt(str[8]);
            fatcats.put(temp, value);
            if (fatcats.size() > K)
                fatcats.remove(fatcats.firstKey())
        }
        @Override
        protected void cleanup(Context context) throws IOException,  InterruptedException {
            for(Text text: fatcats.values()){
                context.write(NullWritable.get(), text);
            }
        }
    }

    public static class Reduce extends Reducer<NullWritable, Text, NullWritable, Text> {
        public static final int K = 100;
        private TreeMap<Integer, Text> fatcats = new TreeMap<Integer, Text>();
        public void reduce(NullWritable key, Iterable<Text> values, Context context)
                throws IOException, InterruptedException {
            for (Text val : values) {
                String v[] = val.toString().split("\t");
                Integer weight = Integer.parseInt(v[1]);
                fatcats.put(weight, val);
                if (fatcats.size() > K)
                    fatcats.remove(fatcats.firstKey());
            }
            for (Text text: fatcats.values())
                context.write(NullWritable.get(), text);
        }
    }

    public int run(String[] args) throws Exception {
        Configuration conf = getConf();
        Job job = new Job(conf, "TopKNum");
        job.setJarByClass(Top_k_new.class);
        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        job.setMapperClass(MapClass.class);
       // job.setCombinerClass(Reduce.class);
        job.setReducerClass(Reduce.class);
        job.setInputFormatClass(TextInputFormat.class);
        job.setOutputFormatClass(TextOutputFormat.class);
        job.setOutputKeyClass(NullWritable.class);
        job.setOutputValueClass(Text.class);
        System.exit(job.waitForCompletion(true) ? 0 : 1);
        return 0;
    }
    public static void main(String[] args) throws Exception {
        int res = ToolRunner.run(new Configuration(), new Top_k_new(), args);
        System.exit(res);
    }

}
```