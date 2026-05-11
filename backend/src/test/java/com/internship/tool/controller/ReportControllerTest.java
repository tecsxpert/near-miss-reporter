package com.internship.tool.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
public class ReportControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testGetPageReturns200() throws Exception {
        mockMvc.perform(get("/api/page?page=0&size=5")
               .header("Authorization", "Bearer test-token"))
               .andExpect(status().isOk());
    }

    @Test
    public void testSearchReturns200() throws Exception {
        mockMvc.perform(get("/api/search?q=test&page=0&size=5")
               .header("Authorization", "Bearer test-token"))
               .andExpect(status().isOk());
    }

    @Test
    public void testAddReportReturns200() throws Exception {
        String json = "{\"title\":\"Test\",\"description\":\"Desc\"}";
        mockMvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post("/api/add")
               .header("Authorization", "Bearer test-token")
               .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
               .content(json))
               .andExpect(status().isOk());
    }

    @Test
    public void testUpdateReportReturns200() throws Exception {
        String json = "{\"title\":\"Updated\",\"description\":\"Desc\"}";
        // Assuming ID 1 exists from seeder
        mockMvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put("/api/update/1")
               .header("Authorization", "Bearer test-token")
               .contentType(org.springframework.http.MediaType.APPLICATION_JSON)
               .content(json))
               .andExpect(status().isOk());
    }

    @Test
    public void testDeleteReportReturns200() throws Exception {
        mockMvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete("/api/delete/1")
               .header("Authorization", "Bearer test-token"))
               .andExpect(status().isOk());
    }

    @Test
    public void testFileUploadReturns200() throws Exception {
        org.springframework.mock.web.MockMultipartFile file 
          = new org.springframework.mock.web.MockMultipartFile(
            "file", 
            "test.csv", 
            "text/csv", 
            "Title,Description,Status,Severity,Location\nTest,Test,OPEN,Low,Local".getBytes()
          );

        mockMvc.perform(org.springframework.test.web.servlet.request.MockMvcRequestBuilders.multipart("/api/upload")
               .file(file)
               .header("Authorization", "Bearer test-token"))
               .andExpect(status().isOk());
    }
}
