import java.util.stream.*;
public class HelloWorld {
    public static void main(String []args) {
        // test
        System.out.println(fib(50));
    }
    public static String fib(int n) {
        return Stream.iterate(new long[]{0, 1}, t -> new long[]{t[1], t[0] + t[1]}).limit(n).map(t -> String.valueOf(" ," + t[1])).reduce("", (acc, x) -> acc + x).substring(2);
    }
}