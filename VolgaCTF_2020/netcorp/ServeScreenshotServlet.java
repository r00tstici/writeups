/*     */ package netcorp;
/*     */ 
/*     */ import java.io.File;
/*     */ import java.io.IOException;
/*     */ import java.io.PrintWriter;
/*     */ import java.math.BigInteger;
/*     */ import java.security.MessageDigest;
/*     */ import java.security.NoSuchAlgorithmException;
/*     */ import javax.servlet.ServletConfig;
/*     */ import javax.servlet.ServletException;
/*     */ import javax.servlet.annotation.MultipartConfig;
/*     */ import javax.servlet.http.HttpServlet;
/*     */ import javax.servlet.http.HttpServletRequest;
/*     */ import javax.servlet.http.HttpServletResponse;
/*     */ import javax.servlet.http.Part;
/*     */ import ru.volgactf.netcorp.ServeScreenshotServlet;
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */ @MultipartConfig
/*     */ public class ServeScreenshotServlet
/*     */   extends HttpServlet
/*     */ {
/*     */   private static final String SAVE_DIR = "uploads";
/*     */   
/*  27 */   public ServeScreenshotServlet() { System.out.println("ServeScreenshotServlet Constructor called!"); }
/*     */ 
/*     */ 
/*     */   
/*  31 */   public void init(ServletConfig config) throws ServletException { System.out.println("ServeScreenshotServlet \"Init\" method called"); }
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*  36 */   public void destroy() { System.out.println("ServeScreenshotServlet \"Destroy\" method called"); }
/*     */ 
/*     */ 
/*     */ 
/*     */ 
/*     */   
/*     */   protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
/*  43 */     String appPath = request.getServletContext().getRealPath("");
/*     */ 
/*     */     
/*  46 */     String savePath = appPath + "uploads";
/*     */     
/*  48 */     File fileSaveDir = new File(savePath);
/*  49 */     if (!fileSaveDir.exists()) {
/*  50 */       fileSaveDir.mkdir();
/*     */     }
/*  52 */     String submut = request.getParameter("submit");
/*  53 */     if (submut == null || !submut.equals("true"));
/*     */ 
/*     */     
/*  56 */     for (Part part : request.getParts()) {
/*  57 */       String fileName = extractFileName(part);
/*     */       
/*  59 */       fileName = (new File(fileName)).getName();
/*  60 */       String hashedFileName = generateFileName(fileName);
/*  61 */       String path = savePath + File.separator + hashedFileName;
/*  62 */       if (path.equals("Error"))
/*     */         continue; 
/*  64 */       part.write(path);
/*     */     } 
/*     */     
/*  67 */     PrintWriter out = response.getWriter();
/*  68 */     response.setContentType("application/json");
/*  69 */     response.setCharacterEncoding("UTF-8");
/*  70 */     out.print(String.format("{'success':'%s'}", new Object[] { "true" }));
/*  71 */     out.flush();
/*     */   }
/*     */   
/*     */   private String generateFileName(String fileName) {
/*     */     try {
/*  76 */       MessageDigest md = MessageDigest.getInstance("MD5");
/*  77 */       md.update(fileName.getBytes());
/*  78 */       byte[] digest = md.digest();
/*  79 */       String s2 = (new BigInteger(1, digest)).toString(16);
/*  80 */       StringBuilder sb = new StringBuilder(32);
/*     */       
/*  82 */       for (int i = 0, count = 32 - s2.length(); i < count; i++) {
/*  83 */         sb.append("0");
/*     */       }
/*     */       
/*  86 */       return sb.append(s2).toString();
/*     */     }
/*  88 */     catch (NoSuchAlgorithmException e) {
/*  89 */       e.printStackTrace();
/*  90 */       return "Error";
/*     */     } 
/*     */   }
/*     */   
/*     */   private String extractFileName(Part part) {
/*  95 */     String contentDisp = part.getHeader("content-disposition");
/*  96 */     String[] items = contentDisp.split(";");
/*  97 */     for (String s : items) {
/*  98 */       if (s.trim().startsWith("filename")) {
/*  99 */         return s.substring(s.indexOf("=") + 2, s.length() - 1);
/*     */       }
/*     */     } 
/* 102 */     return "";
/*     */   }
/*     */ }
