package csi3370.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class HomeController {

    @GetMapping("/")
    public String home() {
        return """
               <html>
                   <head>
                       <title>My First Spring Boot App</title>
                   </head>
                   <body>
                       <h1>Hello, Spring Boot 👋</h1>
                       <p>No more white page error.</p>
                   </body>
               </html>
               """;
    }
}
