/*    */ package netcorp;
/*    */ 
/*    */ import java.io.IOException;
/*    */ import javax.servlet.ServletConfig;
/*    */ import javax.servlet.ServletException;
/*    */ import javax.servlet.annotation.MultipartConfig;
/*    */ import javax.servlet.http.HttpServlet;
/*    */ import javax.servlet.http.HttpServletRequest;
/*    */ import javax.servlet.http.HttpServletResponse;
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ 
/*    */ @MultipartConfig
/*    */ public class ServeComplaintServlet
/*    */   extends HttpServlet
/*    */ {
/*    */   private static final long serialVersionUID = 1L;
/*    */   private static final String SAVE_DIR = "uploads";
/*    */   
/* 22 */   public ServeComplaintServlet() { System.out.println("ServeScreenshotServlet Constructor called!"); }
/*    */ 
/*    */ 
/*    */ 
/*    */   
/* 27 */   public void init(ServletConfig config) throws ServletException { System.out.println("ServeScreenshotServlet \"Init\" method called"); }
/*    */ 
/*    */ 
/*    */ 
/*    */   
/* 32 */   public void destroy() { System.out.println("ServeScreenshotServlet \"Destroy\" method called"); }
/*    */   
/*    */   protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {}
/*    */   
/*    */   protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {}
/*    */ }

