# 🚀 **设计模式字典 - 中文版**

https://draveness.me/holy-grail-design-pattern/

https://www.cnblogs.com/wxdlut/p/17346906.html

https://developer.aliyun.com/article/342530

https://www.infoq.cn/article/design-patterns-proposed-by-gof-20-years-ago

## 💭 **关于设计模式的争议**

近年来，关于设计模式的争论非常激烈。

**理解和学习它是第一步（如果你想谈论它，无论你站在哪一边）。**

站在巨人的肩膀上无疑是一个明智的选择。作为经验的汇集，无疑见证了前辈们是如何运用面向对象编程（OOP）思想的。这23篇经验汇集展现了一段辉煌的历史。

**如何应用它是第二步，而分歧也由此而来。**
有些人将设计模式奉为天堂，认为它们是最佳实践，并被广泛使用。
另一些人则将设计模式贬低为地狱，认为它们不过是过去的糟粕，并不适用于当下。
当然，大多数人持中立态度。

**尽信书不如无书。追求低耦合，但不可能完全没有耦合。**

首先，在实际应用中考虑使用设计模式并没有错。这只是利用现有的解决方案来解决现有的问题。

然而，在分析和处理问题时，并不应该局限于设计模式。设计模式是面向对象编程（OOP）思维的最佳实践，也就是说，OOP 的落地经验产生了设计模式。

面对实际问题时，OOP 思维应该是第一反应。在 OOP 思维下，问题才有一个对应的上下文。这些上下文就是设计模式的源泉。同时，可以考虑当前问题是否与设计模式中已经解决的问题相匹配。

**OOP和设计模式的比喻：乘法规则 / 25*25 = 625**

接下来，也是最重要的一步 —— **平衡 与取舍** 。
这是把握设计与过度设计的关键一步，关键在于**利大于弊**。

设计模式并不能解决所有问题，反而会带来新的问题。但如果解决问题的价值大于新问题的弊端，那就使用它。

这条规则似乎不仅限于设计模式，所有方法论都适用。**动态地分析问题处理方式的优劣，是为了达到一个准确合理的终点。**

## 🏗️ **创建对象的模式**

## 🔒 **单例模式**

全局唯一；通过添加类似 @Component 的注解，Spring bean 的作用域为单例。

## 🧬 **原型模式**

通过复制旧对象创建对象；为 Spring bean 设置 @Scope("prototype")。

## 🏗️ **建造者模式**

使用建造者模式创建复杂对象，无需在构造函数中传递大量参数；为对象添加 Lombok 的 @Builder 注解。

## 🏭 **工厂模式**

封装一组或多组对象的创建过程，并提供统一的参数化对象创建入口。[结合策略模式实现]

- 工厂方法
- 抽象工厂 —— 工厂的工厂

## 🎭 **对象行为模式**

## 🎯 **策略模式**

**背景**：对于对象的单一行为，在不同场景下会有不同的实现。

**思路**：添加策略层（策略接口），解耦程序调用与实现，实现程序的可扩展性。

**Implemention**: https://github.com/qiao-925/Strategy-pattern-demo

## 📋 **模板模式**

**背景：**对于一组操作，大多数步骤相同，只有少数步骤不同，这将产生大量重复代码。

**思路**：定义程序的框架，并将部分步骤推迟到子类中，以实现模板代码复用。

## 👁️ **观察者模式**

对象级别的 MQ。

专注于对象级别的事件发布和消息通知

## 🔗 **职责链模式**

根据单一职责原则，将复杂的业务处理流程拆分成链表结构，以实现可读性和可扩展性。

## ⚡ **命令模式**

解耦请求发送者和接收者。

- code example
    
    ```jsx
    // 命令接口
    public interface Command {
        void execute();
    }
    
    // 接收者
    public class Light {
        public void turnOn() {
            System.out.println("The light is on.");
        }
    
        public void turnOff() {
            System.out.println("The light is off.");
        }
    }
    
    // 具体命令：打开灯
    public class TurnOnLightCommand implements Command {
        private Light light;
    
        public TurnOnLightCommand(Light light) {
            this.light = light;
        }
    
        @Override
        public void execute() {
            light.turnOn();
        }
    }
    
    // 具体命令：关闭灯
    public class TurnOffLightCommand implements Command {
        private Light light;
    
        public TurnOffLightCommand(Light light) {
            this.light = light;
        }
    
        @Override
        public void execute() {
            light.turnOff();
        }
    }
    
    // 调用者
    public class RemoteControl {
        private Command command;
    
        public void setCommand(Command command) {
            this.command = command;
        }
    
        public void pressButton() {
            command.execute(); // 执行命令
        }
    }
    
    public class Client {
        public static void main(String[] args) {
            Light light = new Light(); // 创建接收者
            Command turnOn = new TurnOnLightCommand(light); // 创建打开灯的命令
            Command turnOff = new TurnOffLightCommand(light); // 创建关闭灯的命令
    
            RemoteControl remote = new RemoteControl(); // 创建调用者
    
            // 打开灯
            remote.setCommand(turnOn);
            remote.pressButton();
    
            // 关闭灯
            remote.setCommand(turnOff);
            remote.pressButton();
        }
    }
    ```
    

## 备忘录模式

目标：用于对象的历史记录和备份。

示例：用于编辑器，记录和恢复历史状态。

- code example
    
    ```jsx
    public class Originator {
        private String state;
    
        public Originator(String state) {
            this.state = state;
        }
    
        public String getState() {
            return state;
        }
    
        public void setState(String state) {
            this.state = state;
        }
    /**
    * right here
    **/
        **public Memento createMemento() {
            return new Memento(state);
        }
    
        public void restoreMemento(Memento memento) {
            this.state = memento.getState();
        }**
    
        // Inner class for Memento
        public static class Memento {
            private final String state;
    
            public Memento(String state) {
                this.state = state;
            }
    
            public String getState() {
                return state;
            }
        }
    }
    ```
    

---

关于此模式，讨论的是：

如何在不破坏封装性的情况下公开私有成员变量数据？

当然，从私有变为公共很容易，但这会破坏封装性。

**解决方案：对象本身保留创建备份的功能。**

顺便说一句，这与充血模型的思维相关。

[备忘录模式和充血模型比较 —— from manus](https://www.notion.so/from-manus-2536c2e8d0dd80099b22c57b95b968fa?pvs=21)

https://refactoringguru.cn/design-patterns/memento

## **状态模式**

为每个状态及其行为创建类，以减少超过 3 个“if/else”语句的复杂性。

更易读、更易于维护，但类太多。

- comparation
    
    normal implemention:
    
    ```jsx
    public class ContentWithoutState {
        private String status = "草稿"; // 初始状态为草稿
    
        public void publish() {
            if (status.equals("草稿")) {
                status = "待发布";
                System.out.println("内容已提交待发布");
            } else if (status.equals("待发布")) {
                // 模拟发布过程，可能成功或失败
                boolean success = Math.random() < 0.8; // 80%概率成功
                if (success) {
                    status = "已发布";
                    System.out.println("内容发布成功");
                } else {
                    status = "发布失败";
                    System.out.println("内容发布失败");
                }
            } else {
                System.out.println("内容状态不允许发布");
            }
        }
    
        public String getStatus() {
            return status;
        }
    
        public static void main(String[] args) {
            ContentWithoutState content = new ContentWithoutState();
            content.publish();
            System.out.println("当前状态: " + content.getStatus());
            content.publish();
            System.out.println("当前状态: " + content.getStatus());
            content.publish();
            System.out.println("当前状态: " + content.getStatus());
        }
    }
    ```
    
    implementiom by state pattern
    
    ```jsx
    interface ContentStatus {
        void publish(Content content);
    }
    
    class DraftStatus implements ContentStatus {
        @Override
        public void publish(Content content) {
            System.out.println("内容已提交待发布");
            content.setStatus(content.getPendingStatus());
        }
    }
    
    class PendingStatus implements ContentStatus {
        @Override
        public void publish(Content content) {
            boolean success = Math.random() < 0.8; // 80%概率成功
            if (success) {
                System.out.println("内容发布成功");
                content.setStatus(content.getPublishedStatus());
            } else {
                System.out.println("内容发布失败");
                content.setStatus(content.getFailedStatus());
            }
        }
    }
    
    class PublishedStatus implements ContentStatus {
        @Override
        public void publish(Content content) {
            System.out.println("内容已发布，无法再次发布");
        }
    }
    
    class FailedStatus implements ContentStatus {
        @Override
        public void publish(Content content) {
            System.out.println("内容发布失败，请检查错误并重新提交");
        }
    }
    
    public class ContentWithState {
        private ContentStatus status;
        private DraftStatus draftStatus = new DraftStatus();
        private PendingStatus pendingStatus = new PendingStatus();
        private PublishedStatus publishedStatus = new PublishedStatus();
        private FailedStatus failedStatus = new FailedStatus();
    
        public ContentWithState() {
            this.status = draftStatus;
        }
    
        public void publish() {
            status.publish(this);
        }
    
        public void setStatus(ContentStatus status) {
            this.status = status;
        }
    
        public ContentStatus getDraftStatus() { return draftStatus; }
        public ContentStatus getPendingStatus() { return pendingStatus; }
        public ContentStatus getPublishedStatus() { return publishedStatus; }
        public ContentStatus getFailedStatus() { return failedStatus; }
    
        public static void main(String[] args) {
            ContentWithState content = new ContentWithState();
            content.publish();
            content.publish();
            content.publish();
        }
    }
    ```
    

## 访问者模式

将数据结构与作用于它们的算法分离。

- Example by json operations:
    
    ```jsx
    import org.json.JSONObject;
    
    interface JsonVisitor {
        void visit(JSONObject jsonObject);
    }
    
    class PrintJsonVisitor implements JsonVisitor {
        @Override
        public void visit(JSONObject jsonObject) {
            System.out.println("Name: " + jsonObject.getString("name"));
            System.out.println("Age: " + jsonObject.getInt("age"));
            System.out.println("City: " + jsonObject.getString("city"));
        }
    }
    
    class AgeSquareJsonVisitor implements JsonVisitor {
        @Override
        public void visit(JSONObject jsonObject) {
            int age = jsonObject.getInt("age");
            System.out.println("Age squared: " + age * age);
        }
    }
    
    class AgePlusTenJsonVisitor implements JsonVisitor {
        @Override
        public void visit(JSONObject jsonObject) {
            int age = jsonObject.getInt("age");
            System.out.println("Age plus 10: " + (age + 10));
        }
    }
    
    public class JsonWithVisitor {
        public static void main(String[] args) {
            String jsonString = "{\"name\":\"Alice\",\"age\":30,\"city\":\"New York\"}";
            JSONObject jsonObject = new JSONObject(jsonString);
    
            JsonVisitor printVisitor = new PrintJsonVisitor();
            printVisitor.visit(jsonObject);
    
            JsonVisitor ageSquareVisitor = new AgeSquareJsonVisitor();
            ageSquareVisitor.visit(jsonObject);
    
            JsonVisitor agePlusTenVisitor = new AgePlusTenJsonVisitor();
            agePlusTenVisitor.visit(jsonObject);
        }
    }
    ```
    

## 中介者模式

背景：多个对象之间存在大量的相互依赖关系。

其理念与 IOC 非常相似：将对象之间的对话转换为中介者与对象之间的对话。

# 对象结构模式

## **适配器模式**

添加适配层来解决接口不兼容问题。

专注于接口层面。

## 桥接模式

延迟实例化和绑定。

使用组合模式代替继承模式，以避免类的排列组合导致的数量激增。

- 
    
    ```jsx
    // Implementor interface
    interface MessageSender {
        void sendMessage(String message);
    }
    
    // Concrete Implementors
    class EmailSender implements MessageSender {
        @Override
        public void sendMessage(String message) {
            System.out.println("Sending email: " + message);
        }
    }
    
    class SmsSender implements MessageSender {
        @Override
        public void sendMessage(String message) {
            System.out.println("Sending SMS: " + message);
        }
    }
    
    // Abstraction
    abstract class Message {
        protected MessageSender sender;
    
        Message(MessageSender sender) {
            this.sender = sender;
        }
    
        abstract void send(String message);
    }
    
    // Refined Abstractions
    class UrgentMessage extends Message {
        UrgentMessage(MessageSender sender) {
            super(sender);
        }
    
        @Override
        void send(String message) {
            sender.sendMessage("URGENT: " + message);
        }
    }
    
    class NormalMessage extends Message {
        NormalMessage(MessageSender sender) {
            super(sender);
        }
    
        @Override
        void send(String message) {
            sender.sendMessage(message);
        }
    }
    
    // Client code
    public class BridgePatternDemo {
        public static void main(String[] args) {
            MessageSender emailSender = new EmailSender();
            MessageSender smsSender = new SmsSender();
    
            Message urgentEmail = new UrgentMessage(emailSender);
            urgentEmail.send("Meeting at 2 PM");
    
            Message normalSms = new NormalMessage(smsSender);
            normalSms.send("Reminder: Grocery shopping");
        }
    }
    ```
    

## 组合模式

为客户端屏蔽对象和组合对象的具体实现提供统一的处理接口。

- 
    
    ```jsx
    // 抽象组件
    public abstract class TreeNode {
        protected Long id;
        protected Long parentId;
        protected String name;
        protected Integer level;
        protected Integer sort;
        
        // 子节点操作
        public abstract void add(TreeNode node);
        public abstract void remove(TreeNode node);
        public abstract List<TreeNode> getChildren();
        
        // 树形结构操作
        public abstract List<TreeNode> getPath();
        public abstract boolean isLeaf();
        public abstract int getDepth();
    }
    
    // 叶子节点
    public class TreeLeaf extends TreeNode {
        @Override
        public void add(TreeNode node) {
            throw new UnsupportedOperationException("Leaf node cannot add child");
        }
        
        @Override
        public void remove(TreeNode node) {
            throw new UnsupportedOperationException("Leaf node cannot remove child");
        }
        
        @Override
        public List<TreeNode> getChildren() {
            return Collections.emptyList();
        }
        
        @Override
        public List<TreeNode> getPath() {
            return Collections.singletonList(this);
        }
        
        @Override
        public boolean isLeaf() {
            return true;
        }
        
        @Override
        public int getDepth() {
            return 0;
        }
    }
    
    // 分支节点
    public class TreeBranch extends TreeNode {
        private List<TreeNode> children = new ArrayList<>();
        
        @Override
        public void add(TreeNode node) {
            children.add(node);
        }
        
        @Override
        public void remove(TreeNode node) {
            children.remove(node);
        }
        
        @Override
        public List<TreeNode> getChildren() {
            return Collections.unmodifiableList(children);
        }
        
        @Override
        public List<TreeNode> getPath() {
            List<TreeNode> path = new ArrayList<>();
            path.add(this);
            if (!children.isEmpty()) {
                path.addAll(children.get(0).getPath());
            }
            return path;
        }
        
        @Override
        public boolean isLeaf() {
            return children.isEmpty();
        }
        
        @Override
        public int getDepth() {
            if (children.isEmpty()) {
                return 0;
            }
            return 1 + children.stream()
                              .mapToInt(TreeNode::getDepth)
                              .max()
                              .orElse(0);
        }
    }
    ```
    

## **装饰器模式**

动态地为对象添加一些额外的职责。

- 
    
    ```jsx
    // 组件接口
    public interface Coffee {
        double cost();
        String getDescription();
    }
    
    // 具体组件
    public class SimpleCoffee implements Coffee {
        @Override
        public double cost() {
            return 2.0; // 基础咖啡价格
        }
    
        @Override
        public String getDescription() {
            return "Simple Coffee"; // 描述
        }
    }
    
    ----------------------------------------------------------------
    
    // 装饰器
    public abstract class CoffeeDecorator implements Coffee {
        protected Coffee coffee; // 持有一个Coffee对象
    
        public CoffeeDecorator(Coffee coffee) {
            this.coffee = coffee;
        }
    }
    
    // 具体装饰器：牛奶
    public class MilkDecorator extends CoffeeDecorator {
        public MilkDecorator(Coffee coffee) {
            super(coffee);
        }
    
        @Override
        public double cost() {
            return coffee.cost() + 0.5; // 加牛奶的额外费用
        }
    
        @Override
        public String getDescription() {
            return coffee.getDescription() + ", Milk"; // 添加描述
        }
    }
    
    // 具体装饰器：糖
    public class SugarDecorator extends CoffeeDecorator {
        public SugarDecorator(Coffee coffee) {
            super(coffee);
        }
    
        @Override
        public double cost() {
            return coffee.cost() + 0.2; // 加糖的额外费用
        }
    
        @Override
        public String getDescription() {
            return coffee.getDescription() + ", Sugar"; // 添加描述
        }
    }
    
    ---------------------------------------------------------------------------------------
    
    public class CoffeeShop {
        public static void main(String[] args) {
            Coffee coffee = new SimpleCoffee(); // 创建基础咖啡
            System.out.println(coffee.getDescription() + " $" + coffee.cost());
    
            // 添加牛奶装饰
            coffee = new MilkDecorator(coffee);
            System.out.println(coffee.getDescription() + " $" + coffee.cost());
    
            // 添加糖装饰
            coffee = new SugarDecorator(coffee);
            System.out.println(coffee.getDescription() + " $" + coffee.cost());
        }
    }
    ```
    

## **外观模式**

封装子系统功能并提供简单的接口调用。

- 计算机启动示例
    
    ```jsx
    // 子系统类1
    public class CPU {
        public void freeze() {
            System.out.println("CPU is freezing.");
        }
    
        public void jump(long position) {
            System.out.println("CPU is jumping to: " + position);
        }
    
        public void execute() {
            System.out.println("CPU is executing.");
        }
    }
    
    // 子系统类2
    public class Memory {
        public void load(long position, byte[] data) {
            System.out.println("Memory is loading data at position: " + position);
        }
    }
    
    // 子系统类3
    public class HardDrive {
        public byte[] read(long lba, int size) {
            System.out.println("HardDrive is reading data from LBA: " + lba + ", size: " + size);
            return new byte[size]; // 返回模拟数据
        }
    }
    
    // 外观类
    public class ComputerFacade {
        private CPU cpu;
        private Memory memory;
        private HardDrive hardDrive;
    
        public ComputerFacade() {
            this.cpu = new CPU();
            this.memory = new Memory();
            this.hardDrive = new HardDrive();
        }
    
        public void startComputer() {
            cpu.freeze();
            memory.load(0, hardDrive.read(0, 1024));
            cpu.jump(0);
            cpu.execute();
        }
    }
    
    public class Client {
        public static void main(String[] args) {
            ComputerFacade computer = new ComputerFacade();
            computer.startComputer(); // 启动计算机
        }
    }
    ```
    

## 享元模式

**也称为：** 缓存

通过构建映射实现对象重用。

- 
    
    ```jsx
    // 享元接口
    public interface Shape {
        void draw(String color);
    }
    
    // 具体享元类
    public class Circle implements Shape {
        private String type; // 内部状态
    
        public Circle() {
            this.type = "Circle"; // 共享的状态
        }
    
        @Override
        public void draw(String color) {
            System.out.println("Drawing a " + color + " " + type);
        }
    }
    
    // 享元工厂
    import java.util.HashMap;
    import java.util.Map;
    
    public class ShapeFactory {
        private Map<String, Shape> shapes = new HashMap<>();
    
        public Shape getCircle(String color) {
            Shape circle = shapes.get(color);
            if (circle == null) {
                circle = new Circle();
                shapes.put(color, circle);
                System.out.println("Creating a new circle of color: " + color);
            }
            return circle;
        }
    }
    
    // 客户端代码
    public class Client {
        public static void main(String[] args) {
            ShapeFactory shapeFactory = new ShapeFactory();
    
            // 创建并使用享元对象
            Shape redCircle = shapeFactory.getCircle("Red");
            redCircle.draw("Red");
    
            Shape greenCircle = shapeFactory.getCircle("Green");
            greenCircle.draw("Green");
    
            // 共享相同的对象
            Shape anotherRedCircle = shapeFactory.getCircle("Red");
            anotherRedCircle.draw("Red");
    
            // 输出结果
            System.out.println("Red circle and another red circle are the same object: " + (redCircle == anotherRedCircle));
        }
    }
    ```
    

## 代理模式

创建一个代理对象来控制对真实对象的调用，以实现额外的功能。

- 
    
    ```jsx
    // 主题接口
    public interface Subject {
        void request();
    }
    
    // 真实对象
    public class RealSubject implements Subject {
        @Override
        public void request() {
            System.out.println("RealSubject: Handling request.");
        }
    }
    
    // 代理对象
    public class Proxy implements Subject {
        private RealSubject realSubject;
    
        @Override
        public void request() {
            if (realSubject == null) {
                realSubject = new RealSubject(); // 延迟加载
            }
            // 代理的额外功能
            System.out.println("Proxy: Pre-processing request.");
            realSubject.request(); // 调用真实对象的方法
            System.out.println("Proxy: Post-processing request.");
        }
    }
    
    // 客户端代码
    public class Client {
        public static void main(String[] args) {
            Subject subject = new Proxy(); // 使用代理对象
            subject.request(); // 通过代理对象调用请求
        }
    }
    ```
    

**代理模式与装饰器模式的区别**：实现方式类似，但目标不同：
代理：专注于调用对象的控制。
装饰器：专注于功能扩展。

```
action test 001
```