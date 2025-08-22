# 🚀 **Building a Design Pattern Dictionary**

# Ref

https://draveness.me/holy-grail-design-pattern/

https://www.cnblogs.com/wxdlut/p/17346906.html

https://developer.aliyun.com/article/342530

https://www.infoq.cn/article/design-patterns-proposed-by-gof-20-years-ago

# Opinion about design patterns

Background: In recent years, there has been a lot of debate about design patterns.

**Understanding and learning it is the first step （if you want to talk about it whatever sides）.**

It is undoubtedly a wise choice to stand on the shoulders of giants. As a collection of experiences, we have seen how our predecessors used OOP thinking. These 23 collected experiences have shown us a glorious history.

**How to apply it is the second step, and this is where the differences also come from.**
Some voices regard design patterns as heaven, believing that these are the best practices and use it everywhere.
Other voices degrade design patterns to hell, believing that they are nothing more than the dregs of predecessors and are not applicable to the present.
Of course, the majority are neutral.

**It is better to have no books than to believe in them blindly. It is impossible to have no coupling at all in pursuit of low coupling.**

First of all, there is nothing wrong with considering the use of design patterns in practical applications. This is just using existing solutions to solve existing problems.

However, in the analysis and handling of problems, we should not be limited to design patterns. Design patterns are the best practices of OOP thinking, which means that OOP produces design patterns.

When facing practical problems, OOP thinking should be the first reaction, so that there is a context for the problem under OOP thinking. These contexts are the source of the design pattern. At the same time, we can consider whether the current problem is matched with the problem that has been solved in the design pattern.

Then, the next step is the most important step: balance.
This is the key step to grasp the design and over-design, and the key point is whether **the benefits outweigh the disadvantages.**
Design patterns cannot solve all problems, but will bring new problems. But if the value of solving the problem is greater than the disadvantages of the new problem. Then use it.

This rule does not seem to be limited to design patterns, but all methodologies. **For individuals, the dynamic analysis of the pros and cons of the problem is to reach an accurate and reasonable end point.**

# Patterns for create object

## Singleton

Globally unique；Spring bean`s scope is singleton by adding annotation like @Component.

## Prototype

Create object by coping old one；Set @Scope("prototype") for Spring bean.

## Builder

Friendly to create complicated object by builder pattern instead of many params in constructor；Add @Builder Annotation of Lombok for object.

## Factory

Encapsulates the creation process of one or more groups of objects and provides a unified parameterized object creation entry.[Talk the implemention with strategy pattern]

# Patterns for object behavior

## Strategy pattern

**Background**: For a single behavior of an object, there are different implementations in different scenarios.

**Thinking**: Add a strategy layer (strategy interface) to decouple program calling and implementation and achieve program scalability.

**Implemention**: https://github.com/qiao-925/Strategy-pattern-demo

## Template pattern

**Background：**For a set of operations, most of the steps are the same, and a few steps are different, which will generate a lot of duplicate code.

**Thinking**: Define the skeleton of a program and defer some steps to subclasses to achieve template code reuse.

## Observer pattern

Object level `s MQ.

Focus on event publishing and message notification at the object level

## **Chain of responsibility pattern**

According to the single responsibility principle, complex business processing flows are divided into linked list structures to achieve readable and scalable features.

## Command pattern

Decoupling request senders and receivers.

- 
    
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
    

## Memento pattern

Goal：For history and backup of object.

Example: For editors, record and restore the history state.

Implemention：

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

About this pattern, it`s talk about :

How to expose private member variable data **without breaking encapsulation**? 

Of course, it's easy to go from private to public, but that breaks encapsulation.

**Solution: The object itself retains the function of creating a backup.**

Btw， it`s realted with Hyperemia Model thinking.

https://refactoringguru.cn/design-patterns/memento

## **State pattern**

Create class for every state and behavior of state to decrease the complex of  more than 3 “if/else”. 

More readable and matainable but lots of classes.

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
    

## Visitor pattern

Separate data structures from algorithms that act on them.

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
    

## Mediator pattern

Background: There are a lot of interdependencies between multiple objects. 

The idea is quite similar to IOC: convert the conversation between objects to the conversation between mediator and objects.

# Patterns for object structure

## **Adapter pattern**

Adding an adaptation layer to solve interface incompatibility issues.

Focus on the interface level.

## Bridge pattern

Lazy instantiation and binding.

Use combination instead of inheritance to avoid the explosion of number caused by class permutations and combinations.

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
    

## Composite pattern

Provide a unified processing interface for the specific implementation of client shielding objects and combined objects.

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
    

## **Decorator pattern**

Dynamically add some additional responsibilities to an object.

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
    

## **Facade pattern**

Encapsulate subsystem functions and provide simple interface calls.

- Example by computer start
    
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
    

## Flyweight pattern

**Also known as:** Cache

Object reuse by build map.

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
    

## Proxy pattern

Create a proxy object to control calls to the real object to implement additional functionality.

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
    

**Diff between proxy pattern and decorator pattern,** similar implemention, but diff goals:

proxy: foucs on the control of calling object.

decorator: focus on the function expansion.


```
action test 001
```